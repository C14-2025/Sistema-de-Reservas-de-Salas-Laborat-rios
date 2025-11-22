import type { IBase } from "../interfaces/base";

interface IReservation extends IBase {
  id: string;
  user_email: string;
  lab_id: string;
  lab_name?: string;
  date: string;
  start_time: string;
  end_time: string;
  status: string;
}

export type { IReservation };
