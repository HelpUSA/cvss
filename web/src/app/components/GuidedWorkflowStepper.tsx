type Step = {
  number: number;
  label: string;
};

const STEPS: Step[] = [
  { number: 1, label: "Projeto" },
  { number: 2, label: "Ambiente" },
  { number: 3, label: "Vulnerabilidade" },
  { number: 4, label: "Evidência" },
  { number: 5, label: "Resultado" },
];

export function GuidedWorkflowStepper({
  currentStep,
}: {
  currentStep: number;
}) {
  return (
    <nav
      className="guided-workflow-stepper"
      aria-label="Progresso da avaliação"
    >
      <ol>
        {STEPS.map((step) => {
          const completed =
            step.number < currentStep;
          const current =
            step.number === currentStep;

          return (
            <li
              key={step.number}
              className={
                current
                  ? "is-current"
                  : completed
                    ? "is-complete"
                    : ""
              }
              aria-current={
                current ? "step" : undefined
              }
            >
              <span
                className="guided-workflow-stepper__number"
                aria-hidden="true"
              >
                {completed ? "✓" : step.number}
              </span>
              <span>{step.label}</span>
            </li>
          );
        })}
      </ol>
    </nav>
  );
}
