import { products } from '../public/catalog.js';
export function clean(value, max = 200) { return typeof value === 'string' ? value.trim().slice(0, max) : ''; }
export function phoneNumber(value) {
 const bn='০১২৩৪৫৬৭৮৯'; return clean(value,30).replace(/[০-৯]/g,c=>String(bn.indexOf(c))).replace(/[\s-]/g,'').replace(/^\+88/,'');
}
export function validPhone(value) { return /^01[3-9]\d{8}$/.test(value); }
export function normalizeItems(items) {
 if (!Array.isArray(items) || items.length > 30) throw new Error('কার্টে সর্বোচ্চ ৩০ ধরনের পণ্য রাখা যাবে।');
 const seen = new Set();
 return items.map(item=> {
  const p=products.find(p=>p.id===item?.id);
  if(!p || seen.has(p.id) || !Number.isInteger(item.quantity) || item.quantity<1 || item.quantity>10) throw new Error('পণ্যের পরিমাণ ১ থেকে ১০-এর মধ্যে দিন।');
  seen.add(p.id);return {id:p.id,quantity:item.quantity};
 });
}
export function quote(items, location='dhaka') {
 const normalized=normalizeItems(items);
 if (!normalized.length) throw new Error('আপনার কার্ট খালি।');
 if (!['dhaka','outside'].includes(location)) throw new Error('ডেলিভারি এলাকা বেছে নিন।');
 const lines=normalized.map(item=>{const p=products.find(p=>p.id===item.id);return {id:p.id,name:p.name,price:p.price,quantity:item.quantity};});
 const delivery=location==='dhaka'?80:150;
 return {items:lines,delivery,total:lines.reduce((sum,p)=>sum+p.price*p.quantity,0)+delivery};
}
