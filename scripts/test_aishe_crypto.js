const crypto = require('crypto');
const https = require('https');

const PASSPHRASE = '0123456789123456';

function generateKey(saltHex) {
    const salt = Buffer.from(saltHex, 'hex');
    // CryptoJS defaults: SHA1, keySize: 4 words = 16 bytes, iterations: 1000
    return crypto.pbkdf2Sync(PASSPHRASE, salt, 1000, 16, 'sha1');
}

function encryptValue(valueStr) {
    if (!valueStr) return valueStr;
    const iv = crypto.randomBytes(16);
    const salt = crypto.randomBytes(32);
    const key = generateKey(salt.toString('hex'));

    const cipher = crypto.createCipheriv('aes-128-cbc', key, iv);
    let encrypted = cipher.update(String(valueStr), 'utf8', 'base64');
    encrypted += cipher.final('base64');

    const combined = `${iv.toString('hex')}::${salt.toString('hex')}::${encrypted}`;
    return Buffer.from(combined, 'utf8').toString('base64');
}

function decryptValue(encB64) {
    if (!encB64) return encB64;
    try {
        const decoded = Buffer.from(encB64, 'base64').toString('utf8');
        const parts = decoded.split('::');
        if (parts.length !== 3) return encB64;
        const iv = Buffer.from(parts[0], 'hex');
        const saltHex = parts[1];
        const ciphertext = parts[2];

        const key = generateKey(saltHex);
        const decipher = crypto.createDecipheriv('aes-128-cbc', key, iv);
        let decrypted = decipher.update(ciphertext, 'base64', 'utf8');
        decrypted += decipher.final('utf8');
        return decrypted;
    } catch (e) {
        return `DecryptError: ${e.message}`;
    }
}

// Self-test
const sample = 'Madhya Pradesh';
const enc = encryptValue(sample);
const dec = decryptValue(enc);
console.log(`Self test: original='${sample}', decrypted='${dec}', matches=${sample === dec}`);

process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';

// Test requesting AISHE endpoints
const testUrls = [
    `https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory%20/getUniversityList?stateCode=${encodeURIComponent(encryptValue('23'))}&districtcode=&typeid=&surveyYear=${encodeURIComponent(encryptValue('2020'))}`,
    `https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory/getUniversityList?stateCode=${encodeURIComponent(encryptValue('23'))}&districtcode=&typeid=&surveyYear=${encodeURIComponent(encryptValue('2020'))}`,
    `https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory%20/getCollegeList?districtcode=${encodeURIComponent(encryptValue('418'))}&surveyYear=${encodeURIComponent(encryptValue('2020'))}`,
    `https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory/pm-vidya-laxmi`,
    `https://pdf.aishe.nic.in/aisheinstitutemanagement/institutionDirectory%20/pm-vidya-laxmi`
];

async function run() {
    for (const u of testUrls) {
        console.log(`\nTesting: ${u.substring(0, 110)}...`);
        try {
            const res = await fetch(u, {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
                    'Accept': 'application/json, text/plain, */*',
                    'Origin': 'https://dashboard.aishe.gov.in',
                    'Referer': 'https://dashboard.aishe.gov.in/'
                }
            });
            console.log(`Status: ${res.status}`);
            const text = await res.text();
            console.log(`Length: ${text.length}`);
            console.log(`Preview: ${text.substring(0, 300)}`);
            if (text.startsWith('"') && text.length > 50) {
                const decResp = decryptValue(text.replace(/^"|"$/g, ''));
                console.log(`Decrypted response preview: ${decResp.substring(0, 300)}`);
            }
        } catch (err) {
            console.log(`Fetch Error: ${err.message}`);
        }
    }
}

run();
