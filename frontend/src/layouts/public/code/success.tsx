import { FindingT } from "@/api/types"
import * as React from "react"

export type SuccessProps = {
  finding: FindingT
}

const Success: React.FC<SuccessProps> = ({ finding }) => {
  return <>
    <h1 className="text-3xl font-extrabold tracking-tight text-primary mb-2">
      {finding.hint_title}
    </h1>
    {finding.hint_content.split("\n").map((item, key) => (
      <p className="text-justify" key={key}>
        {item}
      </p>
    ))}
  </>
}

export default Success
