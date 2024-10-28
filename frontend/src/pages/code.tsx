import CodeLayout from "@/layouts/public/code"
import type { HeadFC, PageProps } from "gatsby"
import * as React from "react"

// const Page: React.FC<PageProps> = ({ params: { code } }) => {  // for `[code].tsx`, which doesn't work in production build
const Page: React.FC<PageProps> = ({ location }) => {
  const queryParams = new URLSearchParams(location.search)

  return <div>
    <CodeLayout
      code={queryParams.get("code") || ""}
    />
  </div>
}

export default Page

export const Head: HeadFC = () => <title>Scan Quest</title>
