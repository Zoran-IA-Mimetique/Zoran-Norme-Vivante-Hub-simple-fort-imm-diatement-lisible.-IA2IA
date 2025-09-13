#!/usr/bin/env node
const fs = require('fs');
const bom = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
const vex = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
console.log('SBOM components:', (bom.components||[]).length, 'VEX vulns:', (vex.vulnerabilities||[]).length);
