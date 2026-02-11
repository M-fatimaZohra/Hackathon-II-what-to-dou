import type { Metadata } from "next";
import Script from "next/script";
import { Inter } from "next/font/google";
import { Oswald } from "next/font/google";
import { Satisfy } from "next/font/google";
import "./globals.css";
import Navigation from "@/components/Navigation";

const inter = Inter({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

const oswald = Oswald({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

const satisfy = Satisfy({
  subsets: ["latin"],
  display: "swap",
  weight: "400",
});

export const metadata: Metadata = {
  title: "AI Native Todo App",
  description: "A modern todo application with AI capabilities",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link
          rel="stylesheet"
          href="https://cdn.platform.openai.com/deployments/chatkit/chatkit.css"
        />
      </head>
      <body
        className={`${inter.className} antialiased bg-[#FFFBED]`}
        style={inter.style}
      >
        <Script
          src="https://cdn.platform.openai.com/deployments/chatkit/chatkit.js"
          strategy="beforeInteractive"
        />
        <Navigation />
        <main className="pt-16">
          {children}
        </main>
      </body>
    </html>
  );
}
