import * as path from "path"

export const onCreateWebpackConfig = ({ actions }) => {
  actions.setWebpackConfig({
    resolve: {
      alias: {
        "@/api": path.resolve(__dirname, "src/api"),
        "@/components": path.resolve(__dirname, "src/components"),
        "@/layouts": path.resolve(__dirname, "src/layouts"),
        "@/lib/utils": path.resolve(__dirname, "src/lib/utils"),
      },
    },
  })
}
