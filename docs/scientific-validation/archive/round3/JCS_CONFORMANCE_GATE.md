# Web audit receipt - JCS/RFC 8785 gate

The local recursive canonicalizer is an engineering implementation, not by itself proof of formal RFC 8785 conformance.

## Required properties

- recursive object-property sorting;
- array-order preservation;
- ECMAScript-compatible number serialization;
- `-0` normalization consistent with JSON/JCS behavior;
- rejection of NaN and infinities;
- rejection of lone UTF-16 surrogates in keys and values;
- deterministic canonical bytes for semantically identical JSON data;
- UTF-8 SHA-256 over the canonical representation.

## Required validation

Before the public UI or paper says `RFC 8785 conformant`:

1. pin an independent JCS/RFC 8785 test corpus or a well-established implementation;
2. store its revision/version;
3. run the full applicable test set;
4. persist raw results;
5. compare canonical bytes, not merely JSON object equality.

Until that gate passes, use wording such as:

`JCS-compatible canonicalization implementation; formal RFC 8785 conformance pending pinned corpus validation.`
