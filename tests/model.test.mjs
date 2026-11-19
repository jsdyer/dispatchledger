import test from 'node:test';
import assert from 'node:assert/strict';
import { difference } from '../web/model.mjs';
test('published differences preserve negative signs and undefined percentage rates',()=>{
  assert.deepEqual(difference([0,2]),{number:2,percent:null});
  assert.equal(difference([3936,3664]).number,-272);
});
