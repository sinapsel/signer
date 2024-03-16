import { fileURLToPath, URL } from "url";

const root = '../src';
const regPath = (path) => fileURLToPath(new URL(root + path, import.meta.url))

export default {
    alias: [
      {find: '@', replacement: regPath('')},
      {find: '@a', replacement: regPath('/assets')},
      {find: '@r', replacement: regPath('/routers')},
      {find: '@c', replacement: regPath('/components')},
      {find: '@v', replacement: regPath('/views')},
      {find: '@l', replacement: regPath('/layouts')},
      {find: '@h', replacement: regPath('/helpers')}
    ]
}