import { ButtonHTMLAttributes } from "react";
import clsx from "clsx";

export function NeonButton({ className, ...props }: ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      className={clsx(
        "px-4 py-2 rounded-full bg-slate-900 border border-neon-blue text-neon-blue shadow-neon",
        "transition hover:bg-neon-blue/20 focus:outline-none focus:ring-2 focus:ring-neon-pink",
        className
      )}
      {...props}
    />
  );
}
