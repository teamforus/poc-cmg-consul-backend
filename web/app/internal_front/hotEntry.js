const config = require("./config");

module.exports = (...src) => {
	return [
		"webpack-dev-server/client?http://localhost:" + config.devServer.port,
		"webpack/hot/dev-server",
		...src
	]
}