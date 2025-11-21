import { Calendar, Eye, EyeClosed } from "lucide-react";
import { AuthRepository } from "@/api/repository/auth";
import { useContext, useState } from "react";
import { toast } from "sonner";
import type { AuthType } from "@/types/authType";
import { UserRepository } from "@/api/repository/user";
import { UserContext } from "@/api/context/user.context";
import { useNavigate } from "react-router-dom";

export function LoginPage() {
  const [userData, setUserData] = useState<AuthType>({
    email: "",
    password: "",
  });
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [isShowPassword, setIsShowPassword] = useState<boolean>(true);
  const authRepository = new AuthRepository();
  const userRepository = new UserRepository();
  const { setUser } = useContext(UserContext);
  const navigate = useNavigate();

  async function HandleLogin() {
    setIsLoading(true);
    const loadingToastId = toast.loading("Entrando em sua conta...");
    try {
      const data = userData;
      const response = await authRepository.Login(data);
      if (!response) {
        toast.error("Erro inesperado ao tentar fazer login", {
          id: loadingToastId,
        });
        return;
      }

      const userId = response.id;
      const user = await HandleFetchUser(userId);
      if (!user) {
        toast.error("Erro inesperado ao tentar fazer login", {
          id: loadingToastId,
        });
        return;
      }
      setUser(user);
      toast.success("Login realizado com sucesso!", {
        id: loadingToastId,
      });
      navigate("/");
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  }

  async function HandleFetchUser(userId: string) {
    try {
      const response = await userRepository.GetMe(userId);
      if (!response) {
        toast.error("Um erro inesperado ocorreu ao resgatar os seus dados");
        return;
      }

      return response;
    } catch (err) {
      console.error(err);
      toast.error("Um erro inesperado ocorreu ao resgatar os seus dado");
      return;
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
          <span className="text-2xl font-bold">Bem vindo</span>
          <span className="font-extralight text-sm">
            Faça seu login em sua conta
          </span>
        </div>
        <div className="w-full space-y-6">
          <form action="" className="space-y-4">
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
          </form>
          <div className="space-y-4">
            <button
              disabled={isLoading}
              onClick={HandleLogin}
              className="bg-[#003286] w-full px-4 py-2 font-semibold text-white rounded-md
             hover:brightness-80 active:brightness-60
             transition duration-200"
            >
              login
            </button>
            <div className="bg-black/20 w-full h-px" />
            <div className="flex items-center justify-center">
              <span className="text-sm text-center">
                Ainda não possui conta?{" "}
                <a
                  href="#"
                  className="text-[#003286] font-semibold hover:underline hover:brightness-110 active:brightness-75 transition duration-200 cursor-pointer"
                  onClick={() => navigate("/auth/register")}
                >
                  Crie sua conta aqui
                </a>
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
