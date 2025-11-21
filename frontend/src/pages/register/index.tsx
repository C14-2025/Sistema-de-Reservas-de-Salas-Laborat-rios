import { UserRepository } from "@/api/repository/user";
import type { UserType } from "@/types/userType";
import { Calendar, Eye, EyeClosed } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "sonner";

export function RegisterPage() {
  const [userData, setUserData] = useState<Partial<UserType>>({
    name: "",
    email: "",
    password: "",
  });
  const [confirmPassord, setConfirmPassword] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isShowPassword, setIsShowPassword] = useState<boolean>(true);
  const userRepository = new UserRepository();
  const navigate = useNavigate();

  async function HandleRegister() {
    setIsLoading(true);
    const loadingToastId = toast.loading("Criando sua conta...");
    try {
      const data = userData;
      if (data.password !== confirmPassord) {
        toast.error("Erro inesperado ao tentar criar sua conta", {
          id: loadingToastId,
        });
        return;
      }

      const response = await userRepository.Create(data);
      if (!response) {
        toast.error("Erro inesperado ao tentar criar sua conta", {
          id: loadingToastId,
        });
        return;
      }

      toast.success("Conta criada com sucesso!", {
        id: loadingToastId,
      });
      navigate("/auth/login");
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="flex items-center justify-center w-full h-full">
      <div className="bg-white flex flex-col items-start justify-center p-10 rounded-lg border border-[#e4e4e4] gap-4">
        <div className="flex items-center justify-center gap-2">
          <div className="bg-[#003286] p-2 rounded-md text-white">
            <Calendar />
          </div>
          <span className="text-3xl font-bold">Sistema de Reservas</span>
        </div>
        <div className="bg-black/20 w-full h-px" />
        <div className="flex flex-col">
          <span className="text-2xl font-bold">Criar conta</span>
          <span className="font-extralight text-sm">
            Junte-se ao sistema de reserva
          </span>
        </div>
        <div className="w-full space-y-6">
          <form action="" className="space-y-4">
            <div className="flex flex-col gap-px">
              <span className="font-semibold">Nome</span>
              <div className="bg-[#f2f2f2] border border-[#e4e4e4] px-2 py-2 rounded-md focus-within:outline outline-[#7f98c2]">
                <input
                  type="text"
                  id="name"
                  onChange={(e) =>
                    setUserData((prev) => ({ ...prev, name: e.target.value }))
                  }
                  placeholder="Digite aqui o seu email"
                  className="outline-none"
                />
              </div>
            </div>
            <div className="flex flex-col gap-px">
              <span className="font-semibold">Email</span>
              <div className="bg-[#f2f2f2] border border-[#e4e4e4] px-2 py-2 rounded-md focus-within:outline outline-[#7f98c2]">
                <input
                  type="text"
                  id="email"
                  onChange={(e) =>
                    setUserData((prev) => ({ ...prev, email: e.target.value }))
                  }
                  placeholder="Digite aqui o seu email"
                  className="outline-none"
                />
              </div>
            </div>
            <div className="flex flex-col gap-px">
              <span className="font-semibold">Senha</span>
              <div className="bg-[#f2f2f2] border border-[#e4e4e4] px-2 py-2 rounded-md focus-within:outline outline-[#7f98c2] flex items-center">
                <input
                  type={isShowPassword ? "password" : "text"}
                  id="password"
                  onChange={(e) =>
                    setUserData((prev) => ({
                      ...prev,
                      password: e.target.value,
                    }))
                  }
                  placeholder="Digite aqui a sua senha"
                  className="outline-none flex-1"
                />
                <button
                  type="button"
                  onClick={() => setIsShowPassword(!isShowPassword)}
                >
                  {isShowPassword ? <EyeClosed /> : <Eye />}
                </button>
              </div>
            </div>
            <div className="flex flex-col gap-px">
              <span className="font-semibold">Confirmar senha</span>
              <div className="bg-[#f2f2f2] border border-[#e4e4e4] px-2 py-2 rounded-md focus-within:outline outline-[#7f98c2] flex items-center">
                <input
                  type="text"
                  id="confirmPassword"
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Digite aqui a sua senha"
                  className="outline-none flex-1"
                />
              </div>
            </div>
          </form>
          <div className="space-y-4">
            <button
              disabled={isLoading}
              onClick={HandleRegister}
              className="bg-[#003286] w-full px-4 py-2 font-semibold text-white rounded-md
             hover:brightness-80 active:brightness-60
             transition duration-200"
            >
              Cadastrar
            </button>
            <div className="bg-black/20 w-full h-px" />
            <div className="flex items-center justify-center">
              <span className="text-sm text-center">
                Já possui conta?{" "}
                <a
                  href="#"
                  className="text-[#003286] font-semibold hover:underline hover:brightness-110 active:brightness-75 transition duration-200 cursor-pointer"
                  onClick={() => navigate("/auth/login")}
                >
                  Faça login aqui
                </a>
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
