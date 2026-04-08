"""
CWE validation data for the Auto-PoC bug bounty automation pipeline.
Contains a curated set of CWE IDs commonly encountered in web application
security assessments and bug bounty programs.
"""

import re

VALID_CWE_IDS: set[str] = {
    # Injection
    "CWE-77",   # Improper Neutralization of Special Elements used in a Command ('Command Injection')
    "CWE-78",   # Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')
    "CWE-79",   # Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
    "CWE-80",   # Improper Neutralization of Script-Related HTML Tags in a Web Page (Basic XSS)
    "CWE-83",   # Improper Neutralization of Script in Attributes in a Web Page
    "CWE-87",   # Improper Neutralization of Alternate XSS Syntax
    "CWE-88",   # Improper Neutralization of Argument Delimiters in a Command ('Argument Injection')
    "CWE-89",   # Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
    "CWE-90",   # Improper Neutralization of Special Elements used in an LDAP Query ('LDAP Injection')
    "CWE-91",   # XML Injection (aka Blind XPath Injection)
    "CWE-93",   # Improper Neutralization of CRLF Sequences ('CRLF Injection')
    "CWE-94",   # Improper Control of Generation of Code ('Code Injection')
    "CWE-95",   # Improper Neutralization of Directives in Dynamically Evaluated Code ('Eval Injection')
    "CWE-96",   # Improper Neutralization of Directives in Statically Saved Code ('Static Code Injection')
    "CWE-98",   # Improper Control of Filename for Include/Require Statement in PHP Program ('PHP Remote File Inclusion')
    "CWE-99",   # Improper Control of Resource Identifiers ('Resource Injection')
    "CWE-113",  # Improper Neutralization of CRLF Sequences in HTTP Headers ('HTTP Response Splitting')
    "CWE-116",  # Improper Encoding or Escaping of Output
    "CWE-117",  # Improper Output Neutralization for Logs
    "CWE-564",  # SQL Injection: Hibernate
    "CWE-643",  # Improper Neutralization of Data within XPath Expressions ('XPath Injection')
    "CWE-652",  # Improper Neutralization of Data within XQuery Expressions ('XQuery Injection')
    "CWE-917",  # Improper Neutralization of Special Elements used in an Expression Language Statement ('Expression Language Injection')

    # Authentication & Authorization
    "CWE-255",  # Credentials Management Errors
    "CWE-256",  # Plaintext Storage of a Password
    "CWE-257",  # Storing Passwords in a Recoverable Format
    "CWE-259",  # Use of Hard-coded Password
    "CWE-261",  # Weak Encoding for Password
    "CWE-262",  # Not Using Password Aging
    "CWE-263",  # Password Aging with Long Expiration
    "CWE-284",  # Improper Access Control
    "CWE-285",  # Improper Authorization
    "CWE-287",  # Improper Authentication
    "CWE-288",  # Authentication Bypass Using an Alternate Path or Channel
    "CWE-290",  # Authentication Bypass by Spoofing
    "CWE-294",  # Authentication Bypass by Capture-replay
    "CWE-295",  # Improper Certificate Validation
    "CWE-296",  # Improper Following of a Certificate's Chain of Trust
    "CWE-297",  # Improper Validation of Certificate with Host Mismatch
    "CWE-298",  # Improper Validation of Certificate Expiration
    "CWE-300",  # Channel Accessible by Non-Endpoint
    "CWE-302",  # Authentication Bypass by Assumed-Immutable Data
    "CWE-303",  # Incorrect Implementation of Authentication Algorithm
    "CWE-304",  # Missing Critical Step in Authentication
    "CWE-305",  # Authentication Bypass by Primary Weakness
    "CWE-306",  # Missing Authentication for Critical Function
    "CWE-307",  # Improper Restriction of Excessive Authentication Attempts
    "CWE-308",  # Use of Single-factor Authentication
    "CWE-309",  # Use of Password System for Primary Authentication
    "CWE-321",  # Use of Hard-coded Cryptographic Key
    "CWE-522",  # Insufficiently Protected Credentials
    "CWE-523",  # Unprotected Transport of Credentials
    "CWE-549",  # Missing Password Field Masking
    "CWE-620",  # Unverified Password Change
    "CWE-640",  # Weak Password Recovery Mechanism for Forgotten Password
    "CWE-798",  # Use of Hard-coded Credentials

    # Access Control / IDOR
    "CWE-22",   # Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')
    "CWE-23",   # Relative Path Traversal
    "CWE-24",   # Path Traversal: '../filedir'
    "CWE-36",   # Absolute Path Traversal
    "CWE-200",  # Exposure of Sensitive Information to an Unauthorized Actor
    "CWE-201",  # Insertion of Sensitive Information Into Sent Data
    "CWE-209",  # Generation of Error Message Containing Sensitive Information
    "CWE-213",  # Exposure of Sensitive Information Due to Incompatible Policies
    "CWE-639",  # Authorization Bypass Through User-Controlled Key (IDOR)
    "CWE-862",  # Missing Authorization
    "CWE-863",  # Incorrect Authorization

    # CSRF
    "CWE-352",  # Cross-Site Request Forgery (CSRF)

    # SSRF
    "CWE-918",  # Server-Side Request Forgery (SSRF)

    # Open Redirect
    "CWE-601",  # URL Redirection to Untrusted Site ('Open Redirect')

    # File Handling
    "CWE-73",   # External Control of File Name or Path
    "CWE-114",  # Process Control
    "CWE-434",  # Unrestricted Upload of File with Dangerous Type
    "CWE-436",  # Interpretation Conflict
    "CWE-552",  # Files or Directories Accessible to External Parties

    # Cryptography
    "CWE-261",  # Weak Encoding for Password
    "CWE-310",  # Cryptographic Issues
    "CWE-311",  # Missing Encryption of Sensitive Data
    "CWE-312",  # Cleartext Storage of Sensitive Information
    "CWE-313",  # Cleartext Storage in a File or on Disk
    "CWE-315",  # Cleartext Storage of Sensitive Information in a Cookie
    "CWE-316",  # Cleartext Storage of Sensitive Information in Memory
    "CWE-319",  # Cleartext Transmission of Sensitive Information
    "CWE-320",  # Key Management Errors
    "CWE-322",  # Key Exchange without Entity Authentication
    "CWE-323",  # Reusing a Nonce, Key Pair in Encryption
    "CWE-324",  # Use of a Key Past its Expiration Date
    "CWE-325",  # Missing Required Cryptographic Step
    "CWE-326",  # Inadequate Encryption Strength
    "CWE-327",  # Use of a Broken or Risky Cryptographic Algorithm
    "CWE-328",  # Use of Weak Hash
    "CWE-329",  # Generation of Predictable IV with CBC Mode
    "CWE-330",  # Use of Insufficiently Random Values
    "CWE-331",  # Insufficient Entropy
    "CWE-332",  # Insufficient Entropy in PRNG
    "CWE-333",  # Improper Handling of Insufficient Entropy in TRNG
    "CWE-334",  # Small Space of Random Values
    "CWE-335",  # Incorrect Usage of Seeds in Pseudo-Random Number Generator (PRNG)
    "CWE-336",  # Same Seed in Pseudo-Random Number Generator (PRNG)
    "CWE-337",  # Predictable Seed in Pseudo-Random Number Generator (PRNG)
    "CWE-338",  # Use of Cryptographically Weak Pseudo-Random Number Generator (PRNG)
    "CWE-339",  # Small Seed Space in PRNG
    "CWE-340",  # Generation of Predictable Numbers or Identifiers
    "CWE-347",  # Improper Verification of Cryptographic Signature
    "CWE-649",  # Reliance on Obfuscation or Encryption of Security-Relevant Inputs without Integrity Checking

    # Session Management
    "CWE-384",  # Session Fixation
    "CWE-488",  # Exposure of Data Element to Wrong Session
    "CWE-539",  # Use of Persistent Cookies Containing Sensitive Information
    "CWE-613",  # Insufficient Session Expiration
    "CWE-614",  # Sensitive Cookie in HTTPS Session Without 'Secure' Attribute
    "CWE-1004", # Sensitive Cookie Without 'HttpOnly' Flag

    # Input Validation
    "CWE-20",   # Improper Input Validation
    "CWE-116",  # Improper Encoding or Escaping of Output
    "CWE-172",  # Encoding Error
    "CWE-173",  # Improper Handling of Alternate Encoding
    "CWE-174",  # Double Decoding of the Same Data
    "CWE-175",  # Improper Handling of Mixed Encoding
    "CWE-176",  # Improper Handling of Unicode Encoding
    "CWE-180",  # Incorrect Behavior Order: Validate Before Canonicalize
    "CWE-181",  # Incorrect Behavior Order: Validate Before Filter

    # Race Conditions / Logic Errors
    "CWE-362",  # Concurrent Execution using Shared Resource with Improper Synchronization ('Race Condition')
    "CWE-367",  # Time-of-check Time-of-use (TOCTOU) Race Condition
    "CWE-840",  # Business Logic Errors

    # Denial of Service
    "CWE-400",  # Uncontrolled Resource Consumption
    "CWE-401",  # Missing Release of Memory after Effective Lifetime
    "CWE-404",  # Improper Resource Shutdown or Release
    "CWE-407",  # Inefficient Algorithmic Complexity
    "CWE-409",  # Improper Handling of Highly Compressed Data (Data Amplification)
    "CWE-410",  # Insufficient Resource Pool
    "CWE-770",  # Allocation of Resources Without Limits or Throttling
    "CWE-776",  # Improper Restriction of Recursive Entity References in DTDs ('XML Entity Expansion')

    # XXE
    "CWE-611",  # Improper Restriction of XML External Entity Reference ('XXE')
    "CWE-827",  # Improper Control of Document Type Definition

    # Deserialization
    "CWE-502",  # Deserialization of Untrusted Data

    # Security Misconfiguration
    "CWE-16",   # Configuration
    "CWE-260",  # Password in Configuration File
    "CWE-548",  # Exposure of Information Through Directory Listing
    "CWE-611",  # Improper Restriction of XML External Entity Reference
    "CWE-732",  # Incorrect Permission Assignment for Critical Resource
    "CWE-757",  # Selection of Less-Secure Algorithm During Negotiation ('Algorithm Downgrade')
    "CWE-778",  # Insufficient Logging
    "CWE-779",  # Logging of Excessive Data

    # HTTP Security Headers / Browser Issues
    "CWE-116",  # Improper Encoding or Escaping of Output
    "CWE-346",  # Origin Validation Error
    "CWE-348",  # Use of Less Trusted Source
    "CWE-349",  # Acceptance of Extraneous Untrusted Data With Trusted Data
    "CWE-444",  # Inconsistent Interpretation of HTTP Requests ('HTTP Request/Response Smuggling')
    "CWE-451",  # User Interface (UI) Misrepresentation of Critical Information
    "CWE-565",  # Reliance on Cookies without Validation and Integrity Checking
    "CWE-693",  # Protection Mechanism Failure
    "CWE-1021", # Improper Restriction of Rendered UI Layers or Frames (Clickjacking)

    # Supply Chain / Third-Party
    "CWE-829",  # Inclusion of Functionality from Untrusted Control Sphere
    "CWE-830",  # Inclusion of Web Functionality from an Untrusted Source

    # Memory Corruption (relevant for native components in web apps)
    "CWE-119",  # Improper Restriction of Operations within the Bounds of a Memory Buffer
    "CWE-120",  # Buffer Copy without Checking Size of Input ('Classic Buffer Overflow')
    "CWE-121",  # Stack-based Buffer Overflow
    "CWE-122",  # Heap-based Buffer Overflow
    "CWE-125",  # Out-of-bounds Read
    "CWE-126",  # Buffer Over-read
    "CWE-127",  # Buffer Under-read
    "CWE-129",  # Improper Validation of Array Index
    "CWE-131",  # Incorrect Calculation of Buffer Size
    "CWE-190",  # Integer Overflow or Wraparound
    "CWE-191",  # Integer Underflow (Wrap or Wraparound)
    "CWE-416",  # Use After Free
    "CWE-476",  # NULL Pointer Dereference

    # Privilege / Escalation
    "CWE-250",  # Execution with Unnecessary Privileges
    "CWE-266",  # Incorrect Privilege Assignment
    "CWE-269",  # Improper Privilege Management
    "CWE-272",  # Least Privilege Violation
    "CWE-274",  # Improper Handling of Insufficient Privileges
    "CWE-275",  # Permission Issues
    "CWE-276",  # Incorrect Default Permissions
    "CWE-277",  # Insecure Inherited Permissions
    "CWE-278",  # Insecure Preserved Inherited Permissions
    "CWE-279",  # Incorrect Execution-Assigned Permissions
    "CWE-732",  # Incorrect Permission Assignment for Critical Resource

    # Information Disclosure
    "CWE-203",  # Observable Discrepancy
    "CWE-204",  # Observable Response Discrepancy
    "CWE-205",  # Observable Behavioral Discrepancy
    "CWE-208",  # Observable Timing Discrepancy
    "CWE-359",  # Exposure of Private Personal Information to an Unauthorized Actor
    "CWE-497",  # Exposure of Sensitive System Information to an Unauthorized Control Sphere
    "CWE-538",  # Insertion of Sensitive Information into Externally-Accessible File or Directory
    "CWE-540",  # Inclusion of Sensitive Information in Source Code
    "CWE-541",  # Inclusion of Sensitive Information in an Include File
    "CWE-598",  # Use of GET Request Method With Sensitive Query Strings

    # JWT / Token Issues
    "CWE-345",  # Insufficient Verification of Data Authenticity
    "CWE-347",  # Improper Verification of Cryptographic Signature
    "CWE-353",  # Missing Support for Integrity Check
    "CWE-354",  # Improper Validation of Integrity Check Value

    # API Security
    "CWE-285",  # Improper Authorization
    "CWE-441",  # Unintended Proxy or Intermediary ('Confused Deputy')
    "CWE-610",  # Externally Controlled Reference to a Resource in Another Sphere

    # Template Injection
    "CWE-1336", # Improper Neutralization of Special Elements Used in a Template Engine

    # Prototype Pollution / JS-specific
    "CWE-1321", # Improperly Controlled Modification of Object Prototype Attributes ('Prototype Pollution')

    # GraphQL / Modern API
    "CWE-285",  # Improper Authorization (GraphQL auth bypass)
    "CWE-400",  # Uncontrolled Resource Consumption (GraphQL DoS)
}


_CWE_PATTERN = re.compile(r"^CWE-\d+$", re.IGNORECASE)


def validate_cwe_id(cwe_id: str) -> bool:
    """
    Validate that a CWE ID is well-formed and present in the known-valid set.

    A valid CWE ID must:
    - Match the pattern CWE-<number> (case-insensitive format check)
    - Exist in the VALID_CWE_IDS set (exact case match after normalisation)

    Args:
        cwe_id: The CWE ID string to validate (e.g. "CWE-79").

    Returns:
        True if the ID is well-formed and known, False otherwise.
    """
    if not isinstance(cwe_id, str):
        return False
    normalised = cwe_id.strip().upper()
    if not _CWE_PATTERN.match(normalised):
        return False
    return normalised in VALID_CWE_IDS
