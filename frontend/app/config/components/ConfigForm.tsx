/* eslint-disable */
"use client";

import { useRouter } from "next/navigation";


import { useConfig } from "../hooks/useConfig";
import { UserAccountSection } from "./UserAccountSection";

export const ConfigForm = (): JSX.Element => {
  const {
    handleSubmit,
    isDirty,
    maxTokens,
    openAiKey,
    saveConfig,
    register,
    temperature,
    model,
    resetBrainConfig,
  } = useConfig();

  const router = useRouter();

  const handleDoneClick = () => {
    if (isDirty) {
      saveConfig();
    }
    router.back();
  };

  return (
    <form
      className="flex flex-col gap-5 py-5 w-full max-w-xl"
      onSubmit={handleSubmit(handleDoneClick)}
    >
      {/* <ModelConfig
        register={register}
        model={model}
        openAiKey={openAiKey}
        temperature={temperature}
        maxTokens={maxTokens}
      /> */}
      {/* <BackendConfig register={register} /> */}
      {/* <div className="flex justify-between">
        <Button
          variant="danger"
          className="self-end"
          type="button"
          onClick={resetBrainConfig}
        >
          Reset
        </Button>
        <Button variant="secondary" className="self-end">
          Done
        </Button>
      </div> */}
      <UserAccountSection />
    </form>
  );
};
