import type { IBase } from "./base";

interface IUser extends IBase {
  name: string;
  email: string;
}

export type { IUser };
