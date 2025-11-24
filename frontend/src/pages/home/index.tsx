import { UserContext } from "@/api/context/user.context";
import { ReservationRepository } from "@/api/repository/reservation";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { useContext, useEffect, useState } from "react";
import type { IReservation } from "@/api/interfaces/reservation";
import { LabRepository } from "@/api/repository/lab";
import type { ILab } from "@/api/interfaces/lab";
import { toast } from "sonner";

export function HomePage() {
  const { user, logout } = useContext(UserContext);
  const reservationRepository = new ReservationRepository();
  const labRepository = new LabRepository();
  const [reservedLabs, setReservedLabs] = useState<IReservation[]>([]);
  const [availableLabs, setAvailableLabs] = useState<ILab[]>([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState<
    Record<string, { date: string; start_time: string; end_time: string }>
  >({});

  function HandleNameInitials(name: string) {
    const parsedName = name.split(" ");
    return `${parsedName[0]?.[0] || ""}${parsedName[1]?.[0] || ""}`;
  }

  async function HandleListReservedLabs() {
    if (!user?.email) return;
    const result = await reservationRepository.GetByUser(user.email);
    if (result) setReservedLabs(result);
  }

  async function HandleListAvailableLabs() {
    const labs = await labRepository.GetAll();
    if (labs) setAvailableLabs(labs);
  }

  function hasScheduleConflict(
    labId: string,
    schedule: { date: string; start_time: string; end_time: string }
  ) {
    return reservedLabs.some((r) => {
      if (r.lab_id !== labId) return false;
      if (r.date !== schedule.date) return false;
      return (
        schedule.start_time < r.end_time && schedule.end_time > r.start_time
      );
    });
  }

  async function HandleReservation(
    labId: string,
    schedule: { date: string; start_time: string; end_time: string }
  ) {
    if (!user) return;

    if (hasScheduleConflict(labId, schedule)) {
      toast.error("Conflito de horário detectado para este laboratório.");
      return;
    }

    const loadingToast = toast.loading("Criando reserva...");

    try {
      const req = {
        user_email: user.email,
        lab_id: labId,
        date: schedule.date,
        start_time: schedule.start_time,
        end_time: schedule.end_time,
      };

      const created = await reservationRepository.Create(req);

      if (created) {
        toast.success("Reserva criada com sucesso!", { id: loadingToast });
        HandleListReservedLabs();
      } else {
        toast.error("Não foi possível criar a reserva.", { id: loadingToast });
      }
    } catch (err) {
      console.error(err);
      toast.error("Erro inesperado ao criar reserva.", { id: loadingToast });
    }
  }

  function handleLogout() {
    logout();
    window.location.href = "/";
  }

  useEffect(() => {
    async function load() {
      setLoading(true);
      await HandleListAvailableLabs();
      await HandleListReservedLabs();
      setLoading(false);
    }
    load();
  }, []);

  return (
    <section className="flex items-center justify-center w-full h-full gap-8 py-30 px-20">
      <div className="bg-white p-10 rounded-lg border border-[#e4e4e4] flex-1 h-full space-y-10 flex flex-col overflow-hidden">
        <div className="shrink-0 flex items-center justify-between">
          <div className="flex gap-4 items-center justify-start">
            <Avatar className="w-15 h-15">
              {user?.name && (
                <AvatarFallback>{HandleNameInitials(user.name)}</AvatarFallback>
              )}
            </Avatar>
            <div className="flex flex-col items-start justify-center">
              <span className="font-semibold text-2xl">{user?.name}</span>
              <span className="font-thin">{user?.email}</span>
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="text-red-600 hover:underline cursor-pointer"
          >
            Logout
          </button>
        </div>
        <div className="space-y-4 overflow-y-scroll flex-1 pr-2">
          <h2 className="text-xl font-semibold">Laboratórios Reservados</h2>
          {reservedLabs.length === 0 ? (
            <p className="text-gray-400 text-sm">Nenhuma reserva encontrada.</p>
          ) : (
            reservedLabs.map((res) => (
              <div
                key={res.id}
                className="border p-4 rounded-lg shadow-sm bg-gray-50"
              >
                <p>Lab: {res.lab_name}</p>
                <p>Lab id: {res.lab_id}</p>
                <p>Dia: {res.date}</p>
                <p>
                  Horário: {res.start_time} - {res.end_time}
                </p>
                <p>Status: {res.status}</p>
              </div>
            ))
          )}
        </div>
      </div>
      <div className="bg-white p-10 rounded-lg border border-[#e4e4e4] flex-1 h-full overflow-hidden">
        <h2 className="text-xl font-semibold mb-4">Laboratórios Disponíveis</h2>
        <div className="overflow-y-scroll h-full pr-2">
          {availableLabs.length === 0 && !loading && (
            <p className="text-gray-400 text-sm">
              Nenhum laboratório disponível.
            </p>
          )}
          {availableLabs.map((lab) => {
            const data = formData[lab.id] || {
              date: "",
              start_time: "",
              end_time: "",
            };
            function UpdateField(field: string, value: string) {
              setFormData((prev) => ({
                ...prev,
                [lab.id]: { ...prev[lab.id], [field]: value },
              }));
            }
            return (
              <div
                key={lab.id}
                className="border p-6 rounded-lg shadow-sm mb-4 bg-white space-y-4"
              >
                <div>
                  <p className="font-semibold text-lg">{lab.name}</p>
                  <p className="text-sm text-gray-500">{lab.description}</p>
                </div>
                <form className="space-y-4">
                  <div className="flex flex-col gap-px">
                    <span className="font-semibold">Dia da Reserva</span>
                    <div className="bg-[#f2f2f2] border border-[#e4e4e4] px-2 py-2 rounded-md">
                      <input
                        type="date"
                        value={data.date}
                        onChange={(e) => UpdateField("date", e.target.value)}
                        className="outline-none bg-transparent w-full"
                      />
                    </div>
                  </div>
                  <div className="flex flex-col gap-px">
                    <span className="font-semibold">Horário Inicial</span>
                    <div className="bg-[#f2f2f2] border border-[#e4e4e4] px-2 py-2 rounded-md">
                      <input
                        type="time"
                        value={data.start_time}
                        onChange={(e) =>
                          UpdateField("start_time", e.target.value)
                        }
                        className="outline-none bg-transparent w-full"
                      />
                    </div>
                  </div>
                  <div className="flex flex-col gap-px">
                    <span className="font-semibold">Horário Final</span>
                    <div className="bg-[#f2f2f2] border border-[#e4e4e4] px-2 py-2 rounded-md">
                      <input
                        type="time"
                        value={data.end_time}
                        onChange={(e) =>
                          UpdateField("end_time", e.target.value)
                        }
                        className="outline-none bg-transparent w-full"
                      />
                    </div>
                  </div>
                </form>
                <button
                  disabled={!data.date || !data.start_time || !data.end_time}
                  onClick={() =>
                    HandleReservation(lab.id, {
                      date: data.date,
                      start_time: data.start_time,
                      end_time: data.end_time,
                    })
                  }
                  className="bg-[#003286] w-full px-4 py-2 font-semibold text-white rounded-md hover:brightness-90 active:brightness-75 transition duration-200 disabled:opacity-40"
                >
                  Reservar
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
