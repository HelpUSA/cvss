type Bucket = {
  count: number;
  resetAt: number;
};

const buckets =
  new Map<string, Bucket>();

const WINDOW_MS = 60_000;
const LIMIT = 20;

export function consumeDemoRateLimit(
  key: string,
): {
  allowed: boolean;
  remaining: number;
  resetAt: number;
} {
  const now = Date.now();

  const current =
    buckets.get(key);

  if (
    !current ||
    current.resetAt <= now
  ) {
    const bucket = {
      count: 1,
      resetAt:
        now + WINDOW_MS,
    };

    buckets.set(key, bucket);

    return {
      allowed: true,
      remaining:
        LIMIT - 1,
      resetAt:
        bucket.resetAt,
    };
  }

  if (current.count >= LIMIT) {
    return {
      allowed: false,
      remaining: 0,
      resetAt:
        current.resetAt,
    };
  }

  current.count += 1;

  return {
    allowed: true,
    remaining:
      Math.max(
        0,
        LIMIT -
          current.count,
      ),
    resetAt:
      current.resetAt,
  };
}
