import {test,expect} from '@playwright/test';
const origin='http://localhost:8889';
test('actual API rejects invalid input and foreign origins',async({request})=>{
 const config=await request.get(origin+'/api/payment/config');expect(config.status()).toBe(200);expect(typeof (await config.json()).enabled).toBe('boolean');
 const invalidBooking=await request.post(origin+'/api/bookings',{data:{name:'',phone:'123',date:'2000-01-01'}});expect(invalidBooking.status()).toBe(400);
 const invalidOrder=await request.post(origin+'/api/orders',{data:{name:'',paymentMethod:'cod'}});expect(invalidOrder.status()).toBe(400);
 const csrf=await request.put(origin+'/api/cart',{headers:{Origin:'https://unrelated.example'},data:{items:[]}});expect(csrf.status()).toBe(403);
 const notify=await request.post(origin+'/api/payment/notify',{form:{status:'VALID',tran_id:'forged'},maxRedirects:0});expect(notify.status()).toBe(303);expect(notify.headers().location).toContain('payment=pending');
});
