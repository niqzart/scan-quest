import { FindingT } from "@/api/types"
import * as React from "react"

export type SuccessProps = {
  finding: FindingT
}

const Success: React.FC<SuccessProps> = ({ finding }) => {
  return <>
    <h1 className="text-3xl font-extrabold tracking-tight text-primary">
      Code Found!
    </h1>
    <h2 className="text-xl font-bold text-primary">
      {finding.hint_title}
    </h2>
    <p>
      {finding.hint_content}
    </p>
  </>
}

export default Success
