module.exports = {
  transpileDependencies: [],
  productionSourceMap: false,
  filenameHashing: true,
  outputDir: 'build-output',

  publicPath:
    process.env.NODE_ENV === 'production'
      ? '/static/vue/'
      : '/',

  devServer: {
    port: 8080
  }
}