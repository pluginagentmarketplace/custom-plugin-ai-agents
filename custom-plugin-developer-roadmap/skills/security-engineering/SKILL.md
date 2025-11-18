---
name: security-engineering
description: Build secure systems with OWASP Top 10 prevention, threat modeling, authentication/authorization, encryption, and compliance standards. Use when implementing security features and protecting sensitive data.
---

# Security Engineering

Master modern security practices, threat modeling, authentication, encryption, and regulatory compliance.

## Quick Start

### Security First Mindset

```
┌────────────────────────────────────┐
│    Security is Everyone's Job      │
├────────────────────────────────────┤
│ • Developers build secure code     │
│ • Architects design threat models  │
│ • Operations monitor incidents     │
│ • QA tests security scenarios      │
└────────────────────────────────────┘
```

## OWASP Top 10

The ten most critical web application security risks.

### 1. Broken Access Control

Unauthorized users can perform privileged actions.

```typescript
// Bad: No proper authorization check
router.get('/admin/users', (req, res) => {
  // Missing role verification
  const users = db.getAllUsers();
  res.json(users);
});

// Good: Proper authorization
router.get('/admin/users', (req, res) => {
  if (!req.user || req.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }
  const users = db.getAllUsers();
  res.json(users);
});

// Better: Use middleware
const adminOnly = (req, res, next) => {
  if (req.user?.role === 'admin') {
    next();
  } else {
    res.status(403).json({ error: 'Forbidden' });
  }
};

router.get('/admin/users', adminOnly, (req, res) => {
  res.json(db.getAllUsers());
});
```

### 2. Cryptographic Failures

Sensitive data exposed through weak encryption or storage.

```typescript
// Bad: Storing passwords in plaintext
db.save({
  username: 'user',
  password: 'mypassword123'  // NEVER do this!
});

// Bad: Weak hashing
import crypto from 'crypto';
const hash = crypto.createHash('md5').update(password).digest('hex');

// Good: Use bcrypt with salt
import bcrypt from 'bcrypt';
const hashedPassword = await bcrypt.hash(password, 10);

// Good: Encrypt sensitive data in transit
// Use HTTPS/TLS for all communications

// Good: Encrypt sensitive data at rest
const encrypted = await encrypt(sensitiveData, encryptionKey);
db.save({ data: encrypted });
```

### 3. Injection

Malicious input interpreted as code (SQL, NoSQL, Command injection).

```typescript
// Bad: SQL Injection
const userId = req.query.id;
const query = `SELECT * FROM users WHERE id = ${userId}`;
// Input: 1; DROP TABLE users;--
// Becomes: SELECT * FROM users WHERE id = 1; DROP TABLE users;--

// Good: Parameterized queries
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);

// Bad: NoSQL Injection
const user = db.findOne({ username: req.body.username });
// Input: {$ne: null}
// Bypasses authentication!

// Good: Validate and sanitize
const username = String(req.body.username).trim();
if (!/^[a-zA-Z0-9_]+$/.test(username)) {
  throw new Error('Invalid username');
}
const user = db.findOne({ username });

// Bad: Command Injection
const filename = req.query.file;
exec(`cat ${filename}`);
// Input: file.txt; rm -rf /

// Good: Use safe APIs
const fs = require('fs');
fs.readFileSync(filepath);
```

### 4. Insecure Design

Missing or inadequate security controls in design phase.

```typescript
// Example: Weak password reset flow
// Bad design - predictable tokens
const token = Date.now().toString();

// Good design - cryptographically random token
const token = crypto.randomBytes(32).toString('hex');

// Bad design - no rate limiting on login attempts
app.post('/login', (req, res) => {
  // Attackers can brute force
});

// Good design - rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 5  // 5 attempts per window
});

app.post('/login', limiter, (req, res) => {
  // Protected from brute force
});
```

### 5. Broken Authentication

Session/token management vulnerabilities.

```typescript
// Bad: Weak session tokens
const sessionId = userId.toString();  // Predictable!

// Good: Cryptographically secure tokens
const sessionId = crypto.randomBytes(32).toString('hex');

// Bad: No token expiration
const token = jwt.sign({ userId }, secret);  // No expiry!

// Good: Add expiration
const token = jwt.sign(
  { userId },
  secret,
  { expiresIn: '1h' }
);

// Bad: Storing tokens insecurely
localStorage.setItem('token', jwtToken);  // Vulnerable to XSS

// Good: Use httpOnly cookies
res.cookie('token', jwtToken, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 3600000
});
```

### 6. Sensitive Data Exposure

Unnecessary exposure of sensitive information.

```typescript
// Bad: Exposing PII in logs
logger.info(`User ${user.ssn} logged in`);

// Good: Mask sensitive data
logger.info(`User ${user.id} logged in`);

// Bad: Verbose error messages
app.get('/api/user/:id', (req, res) => {
  try {
    const user = db.findById(req.params.id);
    res.json(user);
  } catch (err) {
    // Exposes database structure!
    res.status(500).json({ error: err.message });
  }
});

// Good: Generic error messages
app.get('/api/user/:id', (req, res) => {
  try {
    const user = db.findById(req.params.id);
    res.json(user);
  } catch (err) {
    logger.error(err);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Bad: Returning unnecessary data
const user = {
  id: 1,
  name: 'John',
  email: 'john@example.com',
  passwordHash: '$2b$10$...',  // Never return!
  apiKey: 'secret-key-123'     // Never return!
};

// Good: Return only needed data
const { passwordHash, apiKey, ...safeUser } = user;
res.json(safeUser);
```

## Threat Modeling

Systematic approach to identify and mitigate security risks.

```
Step 1: Identify Assets
├─ User credentials
├─ Payment information
├─ Personal data
└─ Intellectual property

Step 2: Identify Threats
├─ Unauthorized access
├─ Data theft
├─ Service disruption
└─ Data manipulation

Step 3: Identify Vulnerabilities
├─ Weak encryption
├─ No input validation
├─ Missing authentication
└─ Insecure communication

Step 4: Mitigate Risks
├─ Implement controls
├─ Add monitoring
├─ Create incident response
└─ Regular security reviews
```

### STRIDE Model

```
S - Spoofing (Identity)
    Attacker impersonates user
    Mitigation: Strong authentication

T - Tampering (Integrity)
    Attacker modifies data
    Mitigation: Digital signatures, checksums

R - Repudiation (Non-repudiation)
    User denies action they performed
    Mitigation: Audit logs, digital signatures

I - Information Disclosure (Confidentiality)
    Sensitive data exposed
    Mitigation: Encryption, access controls

D - Denial of Service (Availability)
    System becomes unavailable
    Mitigation: Rate limiting, redundancy

E - Elevation of Privilege (Authorization)
    User gains unauthorized access
    Mitigation: RBAC, least privilege
```

## Authentication & Authorization

### Authentication (Who are you?)

```typescript
// Password Authentication
function authenticatePassword(username, password) {
  const user = db.findByUsername(username);
  const isValid = bcrypt.compareSync(password, user.passwordHash);
  if (isValid) {
    return user;
  }
  throw new Error('Invalid credentials');
}

// Multi-Factor Authentication (MFA)
function setupMFA(user) {
  const secret = speakeasy.generateSecret();
  user.mfaSecret = secret;
  return secret.qr_code_url;
}

function verifyMFA(user, token) {
  const verified = speakeasy.totp.verify({
    secret: user.mfaSecret,
    encoding: 'base32',
    token: token,
    window: 2  // 60 second window tolerance
  });
  return verified;
}

// OAuth 2.0 / OpenID Connect
router.get('/auth/google', passport.authenticate('google', {
  scope: ['profile', 'email']
}));

// JWT Tokens
const token = jwt.sign(
  { userId: user.id, email: user.email },
  process.env.JWT_SECRET,
  { expiresIn: '24h' }
);
```

### Authorization (What can you do?)

```typescript
// Role-Based Access Control (RBAC)
enum Role {
  ADMIN = 'admin',
  EDITOR = 'editor',
  VIEWER = 'viewer'
}

const permissions = {
  admin: ['create', 'read', 'update', 'delete'],
  editor: ['create', 'read', 'update'],
  viewer: ['read']
};

function checkPermission(user, action) {
  return permissions[user.role].includes(action);
}

// Attribute-Based Access Control (ABAC)
function checkAccess(user, resource, action) {
  return (
    user.department === resource.department &&  // Attribute
    user.clearanceLevel >= resource.securityLevel && // Attribute
    permissions[user.role].includes(action)  // Role
  );
}

// Middleware example
function authorize(requiredRole) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    if (!checkPermission(req.user, requiredRole)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

router.delete('/posts/:id', authorize('editor'), (req, res) => {
  // Delete post
});
```

## Encryption

### Symmetric Encryption (AES)

```typescript
import crypto from 'crypto';

function encryptData(plaintext, key) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);

  let encrypted = cipher.update(plaintext, 'utf8', 'hex');
  encrypted += cipher.final('hex');

  const authTag = cipher.getAuthTag();

  return {
    iv: iv.toString('hex'),
    encryptedData: encrypted,
    authTag: authTag.toString('hex')
  };
}

function decryptData(encrypted, key) {
  const decipher = crypto.createDecipheriv(
    'aes-256-gcm',
    key,
    Buffer.from(encrypted.iv, 'hex')
  );

  decipher.setAuthTag(Buffer.from(encrypted.authTag, 'hex'));

  let decrypted = decipher.update(encrypted.encryptedData, 'hex', 'utf8');
  decrypted += decipher.final('utf8');

  return decrypted;
}
```

### Asymmetric Encryption (RSA)

```typescript
import crypto from 'crypto';

function generateKeyPair() {
  const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', {
    modulusLength: 2048
  });
  return { publicKey, privateKey };
}

function encryptWithPublicKey(plaintext, publicKey) {
  return crypto.publicEncrypt(publicKey, Buffer.from(plaintext));
}

function decryptWithPrivateKey(encrypted, privateKey) {
  return crypto.privateDecrypt(privateKey, encrypted).toString();
}
```

## Compliance Standards

### GDPR (General Data Protection Regulation)

```
Applies to: EU resident data
Key requirements:
├─ Lawful basis for data processing
├─ Consent management (explicit)
├─ Data subject rights (access, deletion)
├─ Data protection impact assessments
├─ Privacy by design
├─ Data breach notification (72 hours)
└─ Data Protection Officer for certain organizations

Penalties: Up to 20M EUR or 4% revenue
```

### SOC 2 (Service Organization Control)

```
Type I: Security controls in place
Type II: Controls effective over 6+ months

Focus areas:
├─ Security
├─ Availability
├─ Processing Integrity
├─ Confidentiality
└─ Privacy

Requirements:
├─ Access controls
├─ Change management
├─ Monitoring and logging
├─ Encryption
├─ Incident response
└─ Third-party audits
```

### HIPAA (Health Insurance Portability)

```
Applies to: Healthcare data (PHI)
Requirements:
├─ Administrative safeguards
├─ Physical safeguards
├─ Technical safeguards
├─ Encryption of PHI
├─ Access controls and audit logs
└─ Business associate agreements

Penalties: Up to $1.5M per violation category/year
```

## Secure Coding Practices

```typescript
// 1. Input Validation
function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!regex.test(email)) {
    throw new Error('Invalid email');
  }
  return email;
}

// 2. Escape Output
function renderHTML(userInput) {
  return userInput
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
}

// Or use templating engines that auto-escape

// 3. Use Security Headers
app.use((req, res, next) => {
  res.setHeader('X-Content-Type-Options', 'nosniff');
  res.setHeader('X-Frame-Options', 'DENY');
  res.setHeader('X-XSS-Protection', '1; mode=block');
  res.setHeader('Strict-Transport-Security', 'max-age=31536000');
  res.setHeader('Content-Security-Policy', "default-src 'self'");
  next();
});

// 4. Dependency Management
// Regularly update dependencies
// npm audit fix
// Use lock files (package-lock.json)

// 5. Secret Management
const apiKey = process.env.API_KEY;  // From environment
// Never commit secrets to git
// Use .gitignore for .env files
// Consider secret management tools (Vault, AWS Secrets Manager)
```

## Security Checklist

```
Development:
✅ Input validation on all user inputs
✅ Output encoding/escaping
✅ Parameterized queries
✅ Strong password requirements
✅ MFA support
✅ Secure password reset flow
✅ Security headers

Authentication & Authorization:
✅ Strong authentication mechanism
✅ Session management
✅ Token expiration
✅ RBAC or ABAC implementation
✅ Principle of least privilege
✅ Audit logging

Data Protection:
✅ Encryption at rest
✅ Encryption in transit (HTTPS)
✅ Key management strategy
✅ Data retention policies
✅ Sensitive data masking

Operations:
✅ Security monitoring
✅ Intrusion detection
✅ Log retention
✅ Incident response plan
✅ Regular security audits
✅ Penetration testing
✅ Backup and recovery
```

## Best Practices

✅ **Defense in depth** - Multiple layers of security
✅ **Principle of least privilege** - Minimum necessary access
✅ **Security by design** - Not afterthought
✅ **Regular updates** - Patch known vulnerabilities
✅ **Security training** - Keep team aware
✅ **Monitoring** - Detect attacks quickly
✅ **Incident response** - Plan for breaches

## Common Pitfalls

❌ Storing passwords in plaintext
❌ Using weak encryption
❌ No input validation
❌ Hardcoding secrets
❌ Ignoring security warnings
❌ No monitoring/logging
❌ Single authentication method
❌ Not updating dependencies

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)
- [Security Guidelines](https://cheatsheetseries.owasp.org/)
