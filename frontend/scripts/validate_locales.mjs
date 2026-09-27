import fs from 'fs'
import path from 'path'
import { fileURLToPath } from 'url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const localesDir = path.join(__dirname, '../src/i18n/locales')

function flatten(obj, prefix = '') {
  const out = {}
  for (const [k, v] of Object.entries(obj || {})) {
    const key = prefix ? `${prefix}.${k}` : k
    if (v && typeof v === 'object' && !Array.isArray(v)) Object.assign(out, flatten(v, key))
    else out[key] = v
  }
  return out
}

const en = flatten(JSON.parse(fs.readFileSync(path.join(localesDir, 'en.json'), 'utf8')))
const allowSame = new Set([
  'appName',
  'history.live',
  'history.demo',
  'liveAi',
  'settings.api',
  'settings.version',
  'analyze.formatHint',
  'result.map50',
  'result.map5095',
  'result.modelSection',
  'result.classId',
  'auth.loginWithOtp',
  'auth.otpCode',
])

let failed = false
for (const file of fs.readdirSync(localesDir).filter((f) => f.endsWith('.json'))) {
  const code = file.replace('.json', '')
  if (code === 'en') continue
  const flat = flatten(JSON.parse(fs.readFileSync(path.join(localesDir, file), 'utf8')))
  const missing = Object.keys(en).filter((k) => !(k in flat))
  const same = Object.keys(en).filter(
    (k) =>
      flat[k] === en[k] &&
      !allowSame.has(k) &&
      !String(en[k]).includes('BOVIMED') &&
      !String(en[k]).includes('YOLO') &&
      !String(en[k]).includes('JPG, PNG'),
  )
  if (missing.length) {
    console.error(`FAIL ${code}: missing ${missing.length} keys`, missing.slice(0, 8))
    failed = true
  }
  if (same.length) {
    console.error(`FAIL ${code}: ${same.length} keys still identical to English`, same.slice(0, 8))
    failed = true
  }
  if (!missing.length && !same.length) {
    console.log(`OK ${code}`)
  }
}

if (failed) process.exit(1)
const count = fs.readdirSync(localesDir).filter((f) => f.endsWith('.json') && f !== 'en.json').length
console.log(`All ${count} non-English locales validated.`)
