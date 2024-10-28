import { cn } from "@/lib/utils";
import * as React from "react";

export type LoaderProps = {
  size?: number
  className?: string
  svgProps?: React.SVGProps<SVGSVGElement>
}

const LoadingSpinner: React.FC<LoaderProps> = ({
  size = 24,
  className,
  svgProps = {},
}) => {
  return <svg
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={cn("animate-spin", className)}
    {...svgProps}
  >
    <path d="M21 12a9 9 0 1 1-6.219-8.56" />
  </svg>
}

export default LoadingSpinner
