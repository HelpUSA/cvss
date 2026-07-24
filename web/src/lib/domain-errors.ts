export class DomainError extends Error {
  readonly code: string;
  readonly status: number;

  constructor(input: {
    code: string;
    message: string;
    status: number;
  }) {
    super(input.message);

    this.name = "DomainError";
    this.code = input.code;
    this.status = input.status;
  }
}

export function isDomainError(
  error: unknown,
): error is DomainError {
  return error instanceof DomainError;
}
