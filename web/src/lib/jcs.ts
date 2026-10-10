/**
 * RFC 8785 / JSON Canonicalization Scheme helper for JSON-compatible values.
 *
 * Design notes:
 * - Object property names are sorted using JavaScript's default UTF-16 code-unit
 *   ordering, which is the ordering required by JCS for parsed JSON strings.
 * - Numbers use ECMAScript JSON serialization after rejecting non-finite values.
 * - Lone UTF-16 surrogates are rejected in both keys and string values.
 * - Arrays preserve order and are canonicalized recursively.
 *
 * Formal release claims still require execution against a pinned independent
 * JCS/RFC 8785 conformance corpus. This implementation must not be labelled
 * "RFC 8785 conformant" solely because the local contract tests pass.
 */

function assertValidUnicodeScalarSequence(value: string): void {
  for (let i = 0; i < value.length; i += 1) {
    const code = value.charCodeAt(i);
    const isHigh = code >= 0xd800 && code <= 0xdbff;
    const isLow = code >= 0xdc00 && code <= 0xdfff;

    if (isHigh) {
      if (i + 1 >= value.length) {
        throw new TypeError("JCS input contains a lone high surrogate");
      }
      const next = value.charCodeAt(i + 1);
      if (next < 0xdc00 || next > 0xdfff) {
        throw new TypeError("JCS input contains a lone high surrogate");
      }
      i += 1; // consume the matching low surrogate
      continue;
    }

    if (isLow) {
      throw new TypeError("JCS input contains a lone low surrogate");
    }
  }
}

function serializeString(value: string): string {
  assertValidUnicodeScalarSequence(value);
  return JSON.stringify(value);
}

function serializeNumber(value: number): string {
  if (!Number.isFinite(value)) {
    throw new TypeError("JCS input must not contain NaN or Infinity");
  }
  // JSON.stringify follows ECMAScript number serialization and normalizes -0 to 0.
  return JSON.stringify(value);
}

export function jcsCanonicalize(value: unknown): string {
  if (value === null) return "null";

  switch (typeof value) {
    case "boolean":
      return value ? "true" : "false";
    case "string":
      return serializeString(value);
    case "number":
      return serializeNumber(value);
    case "object": {
      if (Array.isArray(value)) {
        return `[${value.map((item) => jcsCanonicalize(item)).join(",")}]`;
      }

      const obj = value as Record<string, unknown>;
      const keys = Object.keys(obj);
      for (const key of keys) assertValidUnicodeScalarSequence(key);
      keys.sort();

      return `{${keys
        .map((key) => `${serializeString(key)}:${jcsCanonicalize(obj[key])}`)
        .join(",")}}`;
    }
    default:
      throw new TypeError(`Unsupported non-JSON value in canonicalization: ${typeof value}`);
  }
}
