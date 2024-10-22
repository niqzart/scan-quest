import * as React from "react"
import type { HeadFC, PageProps } from "gatsby"

const IndexPage: React.FC<PageProps> = () => {
  return <main className="w-screen h-screen content-center text-center">
    <div className=" max-w-[600px] m-auto">
      <h1 className="text-5xl font-extrabold tracking-tight text-primary">
        Title
      </h1>
      <p className="leading-7 [&:not(:first-child)]:mt-4">
        Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one. Line one.
      </p>
      <p className="leading-7 [&:not(:first-child)]:mt-4">
        Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two. Line two.
      </p>
      <div className="text-lg font-semibold mt-4 text-primary">Question</div>
    </div>
  </main>
}

export default IndexPage

export const Head: HeadFC = () => <title>Home Page</title>
