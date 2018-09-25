const webpack = require("webpack");
const WebpackDevServer = require("webpack-dev-server");
const path = require("path");
const config = require("./config");
const webpackConfig = require("./webpack.dev");

const server = new WebpackDevServer(webpack(webpackConfig), {
	publicPath: webpackConfig.output.publicPath,
	hot: true,
	quiet: false,
	stats: { colors: true },
	historyApiFallback: true,
    disableHostCheck: true,
    headers: { 'Access-Control-Allow-Origin': '*' }
});

server.listen(config.devServer.port, "0.0.0.0", (error) => {
	if (error) 
		console.error(error);

	console.info("Listening at localhost:" + config.devServer.port);
});
