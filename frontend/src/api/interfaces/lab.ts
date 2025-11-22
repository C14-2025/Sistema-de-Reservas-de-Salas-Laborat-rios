import type { IBase } from "./base";

interface ILab extends IBase {
  id: string;
  name: string;
  description?: string;
}

export type { ILab };
