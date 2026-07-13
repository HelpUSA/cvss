# Expert-review collection runbook

## Stage 1: reviewer recruitment

1. Identify independent specialists.
2. Send the invitation template.
3. Record qualification data privately.
4. Screen conflicts of interest.
5. Assign a pseudonymous reviewer code.
6. Record agreement acceptance privately.

## Stage 2: package distribution

1. Confirm the assigned packet version.
2. Distribute only the corresponding reviewer ZIP.
3. Do not distribute the answer key.
4. Record the distribution timestamp privately.
5. Ask the reviewer to verify receipt.

## Stage 3: independent review

1. Reviewers work independently.
2. No adjudication discussion is permitted.
3. Reviewers return their response CSV.
4. Preserve the original returned file.
5. Run the response-intake validator.
6. Resolve only structural issues before locking responses.

## Stage 4: response locking

1. Calculate a SHA-256 value for each accepted response.
2. Mark the response as locked.
3. Preserve a read-only copy.
4. Record validation status and lock timestamp.
5. Confirm that all planned reviewers are complete.

## Stage 5: answer-key verification

1. Verify the local answer key against its versioned SHA-256 commitment.
2. Do not alter the answer key before verification.
3. Open the answer key only after independent responses are locked.
4. Preserve the verification output.

## Stage 6: analysis and adjudication

1. Calculate reviewer agreement.
2. Compare reviewers with the watcher candidate values.
3. Conduct structured adjudication.
4. Preserve original and adjudicated decisions.
5. Document disagreement causes.
6. Update the manuscript only after results are verified.
