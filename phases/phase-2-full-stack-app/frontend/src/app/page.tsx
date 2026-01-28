'use client';

import { useRouter } from 'next/navigation';
import { Inter, Satisfy, Oswald } from "next/font/google";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});
const satisfy = Satisfy({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});
const oswald = Oswald({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

export default function Home() {
  const router = useRouter();

  const handleGetStarted = () => {
    router.push('/tasks');
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#FFFBED]">
      <main className="flex flex-col items-center justify-center w-full max-w-3xl p-24">
        <div className="flex flex-col items-center gap-8 text-center">
          <div className="flex flex-col items-center gap-1">
            <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-[#1B1C1C] max-[485px]:text-[1.75rem] max-[349px]:text-[1.65rem]" style={oswald.style}>
              Welcome To
            </h2>
            <h1 className="text-6xl sm:text-7xl md:text-8xl font-bold text-[#1B1C1C] max-[485px]:text-[3.6rem] max-[349px]:text-[3.45rem]" style={satisfy.style}>
              What To Dou
            </h1>
          </div>
          <p className="text-lg text-[#1B1C1C] max-w-md max-[485px]:text-[1.05rem] max-[349px]:text-[1rem]" style={inter.style}>
            A modern todo application that helps you organize your tasks efficiently.
            Get started by creating your tasks.
          </p>
          <button
            onClick={handleGetStarted}
            className="px-6 py-3 bg-[#f2d16f] text-[#1B1C1C] rounded-md hover:bg-[#FFE9A8] transition-colors"
            style={inter.style}
          >
            Get Started
          </button>
        </div>
      </main>
    </div>
  );
}
