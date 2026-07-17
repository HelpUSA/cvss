CREATE SCHEMA IF NOT EXISTS "public";

-- CreateTable
CREATE TABLE "public"."Assessment" (
    "id" TEXT NOT NULL,
    "runId" TEXT NOT NULL,
    "findingId" TEXT NOT NULL,
    "assetId" TEXT NOT NULL,
    "cve" TEXT NOT NULL,
    "vulnerabilityType" TEXT NOT NULL,
    "state" TEXT NOT NULL,
    "baseScore" DOUBLE PRECISION NOT NULL,
    "environmentalScore" DOUBLE PRECISION NOT NULL,
    "cr" TEXT NOT NULL,
    "ir" TEXT NOT NULL,
    "ar" TEXT NOT NULL,
    "mav" TEXT NOT NULL,
    "matchesExpectedRequirements" BOOLEAN NOT NULL,

    CONSTRAINT "Assessment_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."AuditEvent" (
    "id" TEXT NOT NULL,
    "runId" TEXT NOT NULL,
    "ordinal" INTEGER NOT NULL,
    "event" JSONB NOT NULL,

    CONSTRAINT "AuditEvent_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."Comparison" (
    "id" TEXT NOT NULL,
    "runId" TEXT NOT NULL,
    "findingId" TEXT NOT NULL,
    "assetId" TEXT NOT NULL,
    "cve" TEXT NOT NULL,
    "vulnerabilityType" TEXT NOT NULL,
    "environmentalBefore" DOUBLE PRECISION NOT NULL,
    "environmentalAfter" DOUBLE PRECISION NOT NULL,
    "delta" DOUBLE PRECISION NOT NULL,
    "effect" TEXT NOT NULL,
    "mavBefore" TEXT NOT NULL,
    "mavAfter" TEXT NOT NULL,
    "beforeMatchesExpected" BOOLEAN NOT NULL,
    "afterMatchesExpected" BOOLEAN NOT NULL,
    "raw" JSONB NOT NULL,

    CONSTRAINT "Comparison_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "public"."Run" (
    "id" TEXT NOT NULL,
    "caseId" TEXT NOT NULL,
    "generatedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "manifest" JSONB NOT NULL,

    CONSTRAINT "Run_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "Assessment_findingId_idx" ON "public"."Assessment"("findingId" ASC);

-- CreateIndex
CREATE INDEX "Assessment_runId_idx" ON "public"."Assessment"("runId" ASC);

-- CreateIndex
CREATE INDEX "AuditEvent_runId_idx" ON "public"."AuditEvent"("runId" ASC);

-- CreateIndex
CREATE INDEX "Comparison_effect_idx" ON "public"."Comparison"("effect" ASC);

-- CreateIndex
CREATE INDEX "Comparison_runId_idx" ON "public"."Comparison"("runId" ASC);

-- AddForeignKey
ALTER TABLE "public"."Assessment" ADD CONSTRAINT "Assessment_runId_fkey" FOREIGN KEY ("runId") REFERENCES "public"."Run"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "public"."AuditEvent" ADD CONSTRAINT "AuditEvent_runId_fkey" FOREIGN KEY ("runId") REFERENCES "public"."Run"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "public"."Comparison" ADD CONSTRAINT "Comparison_runId_fkey" FOREIGN KEY ("runId") REFERENCES "public"."Run"("id") ON DELETE CASCADE ON UPDATE CASCADE;
