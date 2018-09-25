const webpack = require("webpack");
const path = require("path");
// const HtmlWebpackPlugin = require("html-webpack-plugin");
const BundleTracker = require('webpack-bundle-tracker');

const config = require("./config");
const hotEntry = require("./hotEntry");

const entry = {};
for(let key in config.entry)
	entry[key] = hotEntry(...config.entry[key]);
// const entry = config.entry;

const webpackConfig =  {
	entry: entry,
	output: {
		// path: path.resolve(__dirname, "../../build"),
		// publicPath: "/",
		// filename: "[name].js"
		path: path.resolve("./static/bundles/"),
		filename: "[name]-[hash].js",
		publicPath: "http://localhost:" + config.devServer.port + "/static/bundles/"
	},
	resolve: {
		modules: [
			path.resolve(__dirname, "../templates"),
			"node_modules"
		],
		extensions: [".js"]
	},
	devtool: "cheap-module-source-map",
	module: {
		loaders: [{
			test: /\.(js)?$/,
			loaders: ["babel-loader"]
		},{
			test: /\.json$/,
			loader: ["json-loader"]
		},{
			test: /\.less$/,
			use: [{
				loader: "style-loader"
			}, {
				loader: "css-loader", 
				options: {
					sourceMap: true
				}
			}, {
				loader: "autoprefixer-loader",
				options: {
					browsers: ["last 10 versions", "ie 8"]
				}
			}, {
				loader: "less-loader", 
				options: {
					sourceMap: true,
					paths: [
						path.resolve(__dirname, "../assets"),
						path.resolve(__dirname, "../templates")
					]
				}
			}]
		},{
			test: /\.css$/,
			use: [{
				loader: "style-loader"
			}, {
				loader: "css-loader", 
				options: {
					sourceMap: true
				}
			}]
		},{
            test: /\.pug$/, 
			loader: "pug-loader",
			options: {
				pretty: true,
				//name: '[name].html',
				resolve: {
					alias: {
						templates: path.resolve(__dirname, "../templates"),
						//layouts: path.resolve(__dirname, "../../src/layouts"),
					}
				}
			}
        },{
			test: /\.font\.(js|json)$/,
			use: [{
				loader: "style-loader"
			}, {
				loader: "css-loader", 
				options: {
					sourceMap: true
				}
			}, {
				loader: "fontgen-loader", 
				options: {
					embed: true
				}
			}]
		},{
			test: /\.(png|gif|jpg)$/,
			use: [
				{
					loader: "url-loader",
					options: {
						name: "assets/images/[name].[ext]",
						limit: 1000
					}
				}
			]
		},{
			test: /\.(mp4|webm)$/,
			use: [
				{
					loader: "file-loader",
					options: {
						name: "assets/video/[name].[ext]"
					}
				}
			]
		},{
			test: /\.(eot|ttf|woff|woff2|svg)$/,
			use: [ {
				loader: "file-loader",
				options: {
					name: "assets/fonts/[name].[ext]"
				}
			}]
		}]
	},
	plugins: [
		new BundleTracker({filename: './webpack-stats.json'}),
		new webpack.HotModuleReplacementPlugin(),
		new webpack.NoEmitOnErrorsPlugin()
	]
};



// config.pages.forEach(page => {
// 	webpackConfig.plugins.push(
// 		new HtmlWebpackPlugin({
// 		template: page.src,
// 		filename: page.output
// 		})
// 	);
// });


module.exports = webpackConfig;