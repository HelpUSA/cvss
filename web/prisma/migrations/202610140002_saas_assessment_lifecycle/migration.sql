-- CreateEnum
CREATE TYPE "OperationalAssessmentStatus" AS ENUM ('DRAFT', 'ACTIVE', 'ARCHIVED');

-- CreateEnum
CREATE TYPE "OperationalAssessmentRunStatus" AS ENUM ('COMPLETED', 'ABSTAINED', 'FAILED');

-- CreateEnum
CREATE TYPE "AssessmentReviewDecision" AS ENUM ('APPROVED', 'REJECTED', 'EVIDENCE_REQUESTED');

-- CreateEnum
CREATE TYPE "OrganizationPolicyStatus" AS ENUM ('DRAFT', 'ACTIVE', 'RETIRED');

-- CreateEnum
CREATE TYPE "PlatformSettingStatus" AS ENUM ('ACTIVE', 'RETIRED');

-- CreateTable
CREATE TABLE "OperationalAssessment" (
    "id" TEXT NOT NULL,
    "environmentId" TEXT NOT NULL,
    "vulnerabilityId" TEXT NOT NULL,
    "cve" TEXT,
    "title" TEXT NOT NULL,
    "description" TEXT,
    "status" "OperationalAssessmentStatus" NOT NULL DEFAULT 'DRAFT',
    "createdByUserId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP(3) NOT NULL,
    "archivedAt" TIMESTAMP(3),

    CONSTRAINT "OperationalAssessment_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "EvidenceSnapshot" (
    "id" TEXT NOT NULL,
    "environmentId" TEXT NOT NULL,
    "sourceType" TEXT NOT NULL,
    "sourceReference" TEXT,
    "capturedAt" TIMESTAMP(3) NOT NULL,
    "expiresAt" TIMESTAMP(3),
    "canonicalHash" TEXT NOT NULL,
    "storageReference" TEXT,
    "metadata" JSONB,
    "createdByUserId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "EvidenceSnapshot_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "OperationalAssessmentRun" (
    "id" TEXT NOT NULL,
    "assessmentId" TEXT NOT NULL,
    "executedByUserId" TEXT NOT NULL,
    "status" "OperationalAssessmentRunStatus" NOT NULL,
    "sourceVector" TEXT NOT NULL,
    "sourceScore" DOUBLE PRECISION NOT NULL,
    "finalVector" TEXT,
    "finalScore" DOUBLE PRECISION,
    "severity" TEXT,
    "decision" TEXT NOT NULL,
    "abstentionReasons" JSONB,
    "candidateMetrics" JSONB,
    "operationalDisposition" JSONB,
    "engineCommit" TEXT NOT NULL,
    "ruleCatalogVersion" TEXT,
    "ruleCatalogHash" TEXT,
    "policyId" TEXT,
    "policyVersion" TEXT,
    "evidenceSnapshotId" TEXT NOT NULL,
    "auditReceiptHash" TEXT NOT NULL,
    "startedAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "completedAt" TIMESTAMP(3),
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "OperationalAssessmentRun_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "AssessmentReview" (
    "id" TEXT NOT NULL,
    "runId" TEXT NOT NULL,
    "reviewerUserId" TEXT NOT NULL,
    "decision" "AssessmentReviewDecision" NOT NULL,
    "comments" TEXT,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "AssessmentReview_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "OrganizationPolicyVersion" (
    "id" TEXT NOT NULL,
    "organizationId" TEXT NOT NULL,
    "policyId" TEXT NOT NULL,
    "version" TEXT NOT NULL,
    "contentHash" TEXT NOT NULL,
    "status" "OrganizationPolicyStatus" NOT NULL DEFAULT 'DRAFT',
    "effectiveFrom" TIMESTAMP(3),
    "createdByUserId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "OrganizationPolicyVersion_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "PlatformSetting" (
    "id" TEXT NOT NULL,
    "key" TEXT NOT NULL,
    "version" INTEGER NOT NULL,
    "value" JSONB NOT NULL,
    "status" "PlatformSettingStatus" NOT NULL DEFAULT 'ACTIVE',
    "changedByUserId" TEXT NOT NULL,
    "createdAt" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT "PlatformSetting_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "OperationalAssessment_environmentId_status_idx" ON "OperationalAssessment"("environmentId", "status");

-- CreateIndex
CREATE INDEX "OperationalAssessment_vulnerabilityId_idx" ON "OperationalAssessment"("vulnerabilityId");

-- CreateIndex
CREATE INDEX "OperationalAssessment_cve_idx" ON "OperationalAssessment"("cve");

-- CreateIndex
CREATE INDEX "OperationalAssessment_createdByUserId_idx" ON "OperationalAssessment"("createdByUserId");

-- CreateIndex
CREATE INDEX "OperationalAssessment_createdAt_idx" ON "OperationalAssessment"("createdAt");

-- CreateIndex
CREATE INDEX "EvidenceSnapshot_environmentId_capturedAt_idx" ON "EvidenceSnapshot"("environmentId", "capturedAt");

-- CreateIndex
CREATE INDEX "EvidenceSnapshot_environmentId_canonicalHash_idx" ON "EvidenceSnapshot"("environmentId", "canonicalHash");

-- CreateIndex
CREATE INDEX "EvidenceSnapshot_createdByUserId_idx" ON "EvidenceSnapshot"("createdByUserId");

-- CreateIndex
CREATE INDEX "EvidenceSnapshot_expiresAt_idx" ON "EvidenceSnapshot"("expiresAt");

-- CreateIndex
CREATE INDEX "OperationalAssessmentRun_assessmentId_createdAt_idx" ON "OperationalAssessmentRun"("assessmentId", "createdAt");

-- CreateIndex
CREATE INDEX "OperationalAssessmentRun_executedByUserId_idx" ON "OperationalAssessmentRun"("executedByUserId");

-- CreateIndex
CREATE INDEX "OperationalAssessmentRun_evidenceSnapshotId_idx" ON "OperationalAssessmentRun"("evidenceSnapshotId");

-- CreateIndex
CREATE INDEX "OperationalAssessmentRun_status_idx" ON "OperationalAssessmentRun"("status");

-- CreateIndex
CREATE INDEX "OperationalAssessmentRun_auditReceiptHash_idx" ON "OperationalAssessmentRun"("auditReceiptHash");

-- CreateIndex
CREATE INDEX "AssessmentReview_runId_createdAt_idx" ON "AssessmentReview"("runId", "createdAt");

-- CreateIndex
CREATE INDEX "AssessmentReview_reviewerUserId_createdAt_idx" ON "AssessmentReview"("reviewerUserId", "createdAt");

-- CreateIndex
CREATE INDEX "OrganizationPolicyVersion_organizationId_status_idx" ON "OrganizationPolicyVersion"("organizationId", "status");

-- CreateIndex
CREATE INDEX "OrganizationPolicyVersion_createdByUserId_idx" ON "OrganizationPolicyVersion"("createdByUserId");

-- CreateIndex
CREATE INDEX "OrganizationPolicyVersion_effectiveFrom_idx" ON "OrganizationPolicyVersion"("effectiveFrom");

-- CreateIndex
CREATE UNIQUE INDEX "OrganizationPolicyVersion_organizationId_policyId_version_key" ON "OrganizationPolicyVersion"("organizationId", "policyId", "version");

-- CreateIndex
CREATE INDEX "PlatformSetting_key_status_idx" ON "PlatformSetting"("key", "status");

-- CreateIndex
CREATE INDEX "PlatformSetting_changedByUserId_idx" ON "PlatformSetting"("changedByUserId");

-- CreateIndex
CREATE INDEX "PlatformSetting_createdAt_idx" ON "PlatformSetting"("createdAt");

-- CreateIndex
CREATE UNIQUE INDEX "PlatformSetting_key_version_key" ON "PlatformSetting"("key", "version");

-- AddForeignKey
ALTER TABLE "OperationalAssessment" ADD CONSTRAINT "OperationalAssessment_environmentId_fkey" FOREIGN KEY ("environmentId") REFERENCES "Environment"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OperationalAssessment" ADD CONSTRAINT "OperationalAssessment_createdByUserId_fkey" FOREIGN KEY ("createdByUserId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "EvidenceSnapshot" ADD CONSTRAINT "EvidenceSnapshot_environmentId_fkey" FOREIGN KEY ("environmentId") REFERENCES "Environment"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "EvidenceSnapshot" ADD CONSTRAINT "EvidenceSnapshot_createdByUserId_fkey" FOREIGN KEY ("createdByUserId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OperationalAssessmentRun" ADD CONSTRAINT "OperationalAssessmentRun_assessmentId_fkey" FOREIGN KEY ("assessmentId") REFERENCES "OperationalAssessment"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OperationalAssessmentRun" ADD CONSTRAINT "OperationalAssessmentRun_executedByUserId_fkey" FOREIGN KEY ("executedByUserId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OperationalAssessmentRun" ADD CONSTRAINT "OperationalAssessmentRun_evidenceSnapshotId_fkey" FOREIGN KEY ("evidenceSnapshotId") REFERENCES "EvidenceSnapshot"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AssessmentReview" ADD CONSTRAINT "AssessmentReview_runId_fkey" FOREIGN KEY ("runId") REFERENCES "OperationalAssessmentRun"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "AssessmentReview" ADD CONSTRAINT "AssessmentReview_reviewerUserId_fkey" FOREIGN KEY ("reviewerUserId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OrganizationPolicyVersion" ADD CONSTRAINT "OrganizationPolicyVersion_organizationId_fkey" FOREIGN KEY ("organizationId") REFERENCES "Organization"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "OrganizationPolicyVersion" ADD CONSTRAINT "OrganizationPolicyVersion_createdByUserId_fkey" FOREIGN KEY ("createdByUserId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "PlatformSetting" ADD CONSTRAINT "PlatformSetting_changedByUserId_fkey" FOREIGN KEY ("changedByUserId") REFERENCES "User"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

