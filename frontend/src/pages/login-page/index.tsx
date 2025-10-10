import { GraduationCap } from "lucide-react";

export function LoginPage() {
  return (
    <section className="h-full w-full flex flex-col gap-12 items-center justify-center">
      <div className="gap-4 flex flex-col items-center">
        <GraduationCap className="w-20 h-20" />
        <span className="text-2xl font-bold uppercase w-[300px] text-center">
          Sistema de reserva de salas e laboratórios
        </span>
      </div>
      <div className="flex flex-col gap-4">
        <form className="flex flex-col gap-2">
          <div className="flex flex-col">
            <span>email</span>
            <input
              className="border rounded-sm px-2 py-1"
              placeholder="Digite o seu email"
              type="text"
            />
          </div>
          <div className="flex flex-col">
            <span>senha</span>
            <input
              className="border rounded-sm px-2 py-1"
              placeholder="Digite a sua senha"
              type="text"
            />
          </div>
        </form>
        <button className="bg-[#2463eb] hover:opacity-90 active:opacity-80 py-2 text-[#f1f1f1] rounded-md">
          Login
        </button>
        <button className="bg-[#2463eb] hover:opacity-90 active:opacity-80 py-2 text-[#f1f1f1] rounded-md">
          Cadastro
        </button>
      </div>
    </section>
  );
}
