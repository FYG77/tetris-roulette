import { useEffect } from "react";
import { create } from "zustand";
import { Link } from "react-router-dom";
import { NeonButton } from "../components/NeonButton";
import { useBalance } from "../hooks/useBalance";

interface ThemeState {
  neon: boolean;
  toggle: () => void;
}

const useThemeStore = create<ThemeState>((set) => ({
  neon: true,
  toggle: () => set((state) => ({ neon: !state.neon }))
}));

export default function App() {
  const { data } = useBalance();
  const neon = useThemeStore((state) => state.neon);
  const toggle = useThemeStore((state) => state.toggle);

  useEffect(() => {
    if (neon) {
      document.body.classList.add("neon");
    } else {
      document.body.classList.remove("neon");
    }
  }, [neon]);

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      <header className="px-6 py-4 flex items-center justify-between border-b border-slate-800">
        <h1 className="text-2xl font-semibold tracking-wide text-neon-blue">Tetris Game Roulette</h1>
        <div className="flex items-center gap-4">
          <div className="text-sm text-slate-300">
            Balance: <span className="text-neon-pink font-semibold">{data?.coins ?? "--"}</span>
          </div>
          <NeonButton onClick={toggle}>{neon ? "Lights Down" : "Lights Up"}</NeonButton>
        </div>
      </header>
      <main className="px-6 py-10">
        <section className="max-w-3xl mx-auto bg-slate-900/70 border border-slate-800 rounded-3xl p-8 shadow-neon">
          <h2 className="text-xl font-semibold text-neon-blue mb-4">Skill-based contests</h2>
          <p className="text-slate-300 mb-6">
            Queue up for the next 60 second Tetris showdown. Stake a percentage of your coins and compete to
            climb the leaderboard. Virtual coins only. No cash out. Skill decides the winner.
          </p>
          <div className="grid gap-4 sm:grid-cols-3">
            {[5, 10, 20].map((stake) => (
              <div
                key={stake}
                className="rounded-2xl border border-slate-800 bg-slate-950/80 p-4 text-center hover:border-neon-blue transition"
              >
                <div className="text-sm uppercase text-slate-400">Stake</div>
                <div className="text-3xl font-bold text-neon-purple">{stake}%</div>
                <p className="mt-3 text-xs text-slate-400">Minimum {stake === 5 ? 50 : stake * 10} coins</p>
                <NeonButton className="mt-4 w-full">Join Queue</NeonButton>
              </div>
            ))}
          </div>
          <div className="mt-8 text-xs text-slate-500 uppercase tracking-widest">Test Mode • Skill-Based Contest</div>
        </section>
      </main>
      <footer className="px-6 py-6 border-t border-slate-800 text-xs text-slate-500">
        <div className="flex items-center justify-between">
          <span>© {new Date().getFullYear()} Tetris Game Roulette</span>
          <Link to="/admin" className="hover:text-neon-blue transition">
            Admin Panel
          </Link>
        </div>
      </footer>
    </div>
  );
}
