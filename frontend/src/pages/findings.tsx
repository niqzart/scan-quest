import FindingsLayout from "@/layouts/public/findings"
import type { HeadFC, PageProps } from "gatsby"
import * as React from "react"

const Page: React.FC<PageProps> = () => {
  return <>
    <FindingsLayout />
  </>
}

export default Page

export const Head: HeadFC = () => <title>Findings</title>
