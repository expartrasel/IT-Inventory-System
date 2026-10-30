import type { Config, Context } from '@netlify/functions';
import { eq, and } from 'drizzle-orm';
import { getDb } from '../../db/index.js';
import { carts, orders, bookings } from '../../db/schema.js';
import { clean, phoneNumber, validPhone, normalizeItems, quote } from '../../shared/validation.mjs';

function fail(message: string, status=400) { return Response.json({error:message},{status}); }
function paymentSettings() {
 return {id:Netlify.env.get('SSLCOMMERZ_STORE_ID'), password:Netlify.env.get('SSLCOMMERZ_STORE_PASSWORD'),
 host: Netlify.env.get('SSLCOMMERZ_MODE')==='live'?'https://securepay.sslcommerz.com':'https://sandbox.sslcommerz.com'};
}
function originFor(req: Request) { return new URL(req.url).origin; }
function trustedPost(req: Request) { const origin=req.headers.get('origin');return !origin || origin===originFor(req); }
function session(context: Context) {
 let id=context.cookies.get('two_star_cart');
 if(!id || !/^[a-f0-9-]{36}$/.test(id)) {
  id=crypto.randomUUID();
  context.cookies.set({name:'two_star_cart',value:id,path:'/',httpOnly:true,secure:true,sameSite:'Lax',maxAge:60*60*24*30});
 }
 return id;
}
export default async (req: Request, context: Context) => {
 const route=new URL(req.url).pathname.replace('/api/','');
 const callback=route==='payment/notify';
 if(req.method!=='GET' && !callback && !trustedPost(req))return fail('অনুমোদিত অনুরোধ নয়।',403);
 if(Number(req.headers.get('content-length')||0)>20000)return fail('অনুরোধটি বড়।',413);
 try {
  if(route==='payment/config' && req.method==='GET') {
   const p=paymentSettings();return Response.json({enabled:!!(p.id&&p.password),sandbox:Netlify.env.get('SSLCOMMERZ_MODE')!=='live'});
  }
  if(route==='cart') {
   const db=getDb(),id=session(context);
   if(req.method==='GET') {const [cart]=await db.select().from(carts).where(eq(carts.id,id));return Response.json({items:cart?.items||[]});}
   if(req.method==='PUT') {
    const body=await req.json(),items=normalizeItems(body.items);
    await db.insert(carts).values({id,items}).onConflictDoUpdate({target:carts.id,set:{items,updatedAt:new Date()}});
    return Response.json({items});
   }
  }
  if(route==='bookings' && req.method==='POST') {
   const body=await req.json(),name=clean(body.name,100),phone=phoneNumber(body.phone),device=clean(body.device,30),problem=clean(body.problem,1500),date=clean(body.date,10);
   const today=new Date().toLocaleDateString('en-CA',{timeZone:'Asia/Dhaka'});
   if(name.length<2||!validPhone(phone)||!['ল্যাপটপ','ডেস্কটপ','প্রিন্টার','আপগ্রেড ও সেটআপ','সিসি ক্যামেরা'].includes(device)||problem.length<10||!/^\d{4}-\d{2}-\d{2}$/.test(date)||date<today||Number.isNaN(Date.parse(date)))return fail('নাম, সঠিক মোবাইল নম্বর, সমস্যার বিবরণ ও ভবিষ্যতের তারিখ দিন।');
   const id='TS-S-'+crypto.randomUUID().replaceAll('-','').slice(0,12).toUpperCase();
   await getDb().insert(bookings).values({id,name,phone,device,problem,date});
   return Response.json({id},{status:201});
  }
  if(route==='orders' && req.method==='POST') {
   const body=await req.json(),name=clean(body.name,100),phone=phoneNumber(body.phone),email=clean(body.email,200),address=clean(body.address,1000),paymentMethod=clean(body.paymentMethod,20);
   if(name.length<2||!validPhone(phone)||address.length<10||!/^\S+@\S+\.\S+$/.test(email)||!['cod','online'].includes(paymentMethod))return fail('সঠিক নাম, মোবাইল, ইমেইল ও পূর্ণ ঠিকানা দিন।');
   const settings=paymentSettings();
   if(paymentMethod==='online'&&(!settings.id||!settings.password))return fail('অনলাইন পেমেন্ট এখনো চালু হয়নি। ক্যাশ অন ডেলিভারি বেছে নিন।',409);
   const db=getDb(),sessionId=session(context),[cart]=await db.select().from(carts).where(eq(carts.id,sessionId));
   const prices=quote(cart?.items||[],body.location);
   const id='TS-'+crypto.randomUUID().replaceAll('-','').slice(0,20).toUpperCase();
   await db.insert(orders).values({id,sessionId,name,phone,email,address,paymentMethod,...prices});
   if(paymentMethod==='cod') {
    await db.update(carts).set({items:[],updatedAt:new Date()}).where(eq(carts.id,sessionId));
    return Response.json({id,total:prices.total},{status:201});
   }
   const origin=originFor(req);
   const params=new URLSearchParams({store_id:settings.id!,store_passwd:settings.password!,total_amount:String(prices.total),currency:'BDT',tran_id:id,
    success_url:`${origin}/api/payment/notify`,fail_url:`${origin}/api/payment/notify`,cancel_url:`${origin}/api/payment/notify`,ipn_url:`${origin}/api/payment/notify`,
    cus_name:name,cus_email:email,cus_add1:address,cus_city:body.location==='dhaka'?'Dhaka':'Bangladesh',cus_country:'Bangladesh',cus_phone:phone,
    shipping_method:'YES',ship_name:name,ship_add1:address,ship_city:body.location==='dhaka'?'Dhaka':'Bangladesh',ship_postcode:'1000',ship_country:'Bangladesh',
    product_name:'Two Star Technology IT products',product_category:'Electronics',product_profile:'physical-goods'});
   const gateway=await fetch(`${settings.host}/gwprocess/v4/api.php`,{method:'POST',body:params,signal:AbortSignal.timeout(20000)});
   if(!gateway.ok)return fail(`পেমেন্ট সংযোগে সমস্যা। অর্ডার নম্বর ${id} সংরক্ষণ করুন; পেমেন্টের আগে দোকানের সাথে যোগাযোগ করুন।`,502);
   const result=await gateway.json();
   if(result.status!=='SUCCESS'||!result.GatewayPageURL)return fail(`পেমেন্ট চালু করা যায়নি। অর্ডার নম্বর ${id} সংরক্ষণ করুন।`,502);
   const gatewayUrl=new URL(result.GatewayPageURL);
   if(gatewayUrl.protocol!=='https:' || !['securepay.sslcommerz.com','sandbox.sslcommerz.com'].includes(gatewayUrl.hostname))return fail('পেমেন্ট লিংক পাওয়া যায়নি।',502);
   await db.update(orders).set({status:'awaiting_payment'}).where(eq(orders.id,id));
   return Response.json({id,url:gatewayUrl.href},{status:201});
  }
  if(route==='payment/notify' && req.method==='POST') {
   const data=await req.formData(),valId=clean(data.get('val_id'),100),id=clean(data.get('tran_id'),50),status=clean(data.get('status'),30);
   const redirect=(state:string)=>new Response(null,{status:303,headers:{Location:`${originFor(req)}/?payment=${state}&order=${encodeURIComponent(id)}`}});
   if(!valId || !['VALID','VALIDATED'].includes(status))return redirect('pending');
   const p=paymentSettings();if(!p.id||!p.password)return fail('পেমেন্ট যাচাই চালু নেই।',503);
   const params=new URLSearchParams({val_id:valId,store_id:p.id,store_passwd:p.password,format:'json'});
   const response=await fetch(`${p.host}/validator/api/validationserverAPI.php?${params}`,{signal:AbortSignal.timeout(20000)});
   if(!response.ok)return fail('পেমেন্ট যাচাই সম্পন্ন হয়নি।',502);
   const verified=await response.json(),db=getDb(),[order]=await db.select().from(orders).where(eq(orders.id,id));
   if(!order||order.paymentMethod!=='online'||verified.tran_id!==order.id||!['VALID','VALIDATED'].includes(verified.status)||verified.currency!=='BDT'||Number(verified.amount)!==order.total)return fail('পেমেন্ট যাচাই ব্যর্থ।',400);
   const review=String(verified.risk_level)==='1';
   await db.update(orders).set({paymentStatus:review?'review':'paid',status:review?'payment_review':'confirmed'}).where(eq(orders.id,id));
   // Paid orders are recorded independently; do not erase a cart modified during checkout.
   return redirect(review?'review':'verified');
  }
  if(route==='track' && req.method==='POST') {
   const body=await req.json(),id=clean(body.id,50).toUpperCase(),phone=phoneNumber(body.phone);
   if(!validPhone(phone)||!/^TS-(S-)?[A-F0-9]{12,20}$/.test(id))return fail('সঠিক অর্ডার/বুকিং নম্বর ও মোবাইল দিন।');
   const db=getDb();
   if(id.startsWith('TS-S-')) {
    const [b]=await db.select({id:bookings.id,status:bookings.status,date:bookings.date}).from(bookings).where(and(eq(bookings.id,id),eq(bookings.phone,phone)));
    return b?Response.json({...b,kind:'service'}):fail('এই তথ্য দিয়ে কোনো বুকিং পাওয়া যায়নি।',404);
   }
   const [order]=await db.select({id:orders.id,status:orders.status,paymentStatus:orders.paymentStatus,total:orders.total,createdAt:orders.createdAt}).from(orders).where(and(eq(orders.id,id),eq(orders.phone,phone)));
   return order?Response.json({...order,kind:'order'}):fail('এই তথ্য দিয়ে কোনো অর্ডার পাওয়া যায়নি।',404);
  }
  return fail('এই অনুরোধটি গ্রহণ করা যাচ্ছে না।',405);
 }catch(error) {
  if(error instanceof SyntaxError)return fail('সঠিক তথ্য পাঠান।');
  if(error instanceof Error && ['কার্টে সর্বোচ্চ','পণ্যের পরিমাণ','আপনার কার্ট','ডেলিভারি এলাকা'].some(s=>error.message.startsWith(s)))return fail(error.message);
  return fail('এই মুহূর্তে সংযোগ করা যাচ্ছে না। একটু পরে আবার চেষ্টা করুন।',503);
 }
};
export const config: Config={path:['/api/cart','/api/orders','/api/bookings','/api/track','/api/payment/config','/api/payment/notify']};
