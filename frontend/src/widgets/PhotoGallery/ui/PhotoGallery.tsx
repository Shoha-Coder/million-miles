"use client";

import { useState } from "react";
import Image from "next/image";
import { cn } from "@/shared/lib/cn";

interface PhotoGalleryProps {
  photos: string[];
  alt:    string;
}

export function PhotoGallery({ photos, alt }: PhotoGalleryProps) {
  const [active, setActive] = useState(0);

  if (photos.length === 0) {
    return (
      <div className="flex aspect-[16/9] items-center justify-center rounded-xl bg-gray-100 text-6xl text-gray-300">
        🚗
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {/* Main image */}
      <div className="relative aspect-[16/9] overflow-hidden rounded-xl bg-gray-100">
        <Image
          src={photos[active]}
          alt={alt}
          fill
          sizes="(max-width: 768px) 100vw, 60vw"
          className="object-cover"
          unoptimized
          priority
        />
      </div>

      {/* Thumbnails — only show if more than one photo */}
      {photos.length > 1 && (
        <div className="flex gap-2 overflow-x-auto pb-1">
          {photos.map((src, i) => (
            <button
              key={i}
              onClick={() => setActive(i)}
              className={cn(
                "relative h-16 w-24 shrink-0 overflow-hidden rounded-lg border-2 transition-colors",
                i === active ? "border-brand-500" : "border-transparent hover:border-gray-300",
              )}
              aria-label={`Photo ${i + 1}`}
            >
              <Image
                src={src}
                alt={`${alt} photo ${i + 1}`}
                fill
                sizes="96px"
                className="object-cover"
                unoptimized
              />
            </button>
          ))}
        </div>
      )}
    </div>
  );
}
