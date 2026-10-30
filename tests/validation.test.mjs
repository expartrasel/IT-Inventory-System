import test from 'node:test';
import assert from 'node:assert/strict';
import {quote,normalizeItems,phoneNumber,validPhone} from '../shared/validation.mjs';
test('authoritative prices ignore a submitted price',()=>{const result=quote([{id:'kingston-500',quantity:2,price:1}],'outside');assert.equal(result.total,8650);assert.equal(result.items[0].price,4250);assert.equal(result.delivery,150);});
test('reject invalid, duplicate and excessive quantities',()=>{for(const items of [[{id:'invalid',quantity:1}],[{id:'kingston-500',quantity:0}],[{id:'kingston-500',quantity:11}],[{id:'kingston-500',quantity:1.1}],[{id:'kingston-500',quantity:1},{id:'kingston-500',quantity:2}]])assert.throws(()=>normalizeItems(items));assert.throws(()=>quote([]));assert.throws(()=>quote([{id:'kingston-500',quantity:1}],'unknown'));});
test('Bangla and international Bangladesh phone numbers are normalized',()=>{assert.equal(phoneNumber('+88 ০১৭১২-৩৪৫৬৭৮'),'01712345678');assert.equal(validPhone('01712345678'),true);assert.equal(validPhone('01212345678'),false);});
