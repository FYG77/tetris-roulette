import { useQuery } from "@tanstack/react-query";
import axios from "axios";

interface BalanceResponse {
  coins: number;
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "https://localhost:8000",
  withCredentials: true
});

export function useBalance() {
  return useQuery({
    queryKey: ["balance"],
    queryFn: async (): Promise<BalanceResponse> => {
      const { data } = await api.get<BalanceResponse>("/wallet/balance");
      return data;
    },
    staleTime: 15_000
  });
}
