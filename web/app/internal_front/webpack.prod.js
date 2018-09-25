const webpack = require("webpack");
const path = require("path");

const BundleTracker = require('webpack-bundle-tracker');
// const HtmlWebpackPlugin = require("html-webpack-plugin");
const ExtractTextPlugin = require("extract-text-webpack-plugin");
// const CopyWebpackPlugin = require("copy-webpack-plugin");

const config = require("./config");

const extractStyles = new ExtractTextPlugin('styles/styles.css');
const extractIcons = new ExtractTextPlugin('styles/icons.css');

const webpackConfig = {
	entry: config.entry,
	output: {
		path: path.resolve("assets/dist"),
		filename: "[name].js",
	},
	resolve: {
		modules: [
			path.resolve(__dirname, "../templates"),
			"node_modules"
		],
		extensions: [".js"]
	},
	module: {
		loaders: [{
			test: /\.(js|jsx)?$/,
			loaders: ["babel-loader"],
		}, {
			test: /\.json$/,
			loader: ["json-loader"]
		}, {
			test: /\.less$/,
			use: extractStyles.extract({
				fallback: 'style-loader',
				use: [{
					loader: "css-loader"
				}, {
					loader: "autoprefixer-loader",
					options: {
						browsers: ["last 10 versions", "ie 8"]
					}
				}, {
					loader: "less-loader", 
					options: {
						paths: [
							path.resolve(__dirname, "../assets"),
							path.resolve(__dirname, "../templates")
						]
					}
				}],
			})
		}, {
			test: /\.css$/,
			use: extractStyles.extract({
				fallback: 'style-loader',
				use: [{
					loader: "css-loader"
				}]
			})
		},{
            test: /\.pug$/, 
			loader: "pug-loader",
			options: {
				pretty: true,
				resolve: {
					alias: {
						templates: path.resolve(__dirname, "../templates"),
						// layouts: path.resolve(__dirname, "../../src/layouts"),
					}
				}
			}
        },{
			test: /\.font\.(js|json)$/,
			use: extractIcons.extract({
				fallback: 'style-loader',
				use: [{
					loader: "css-loader",
					options: {
						url: false
					}
				}, {
					loader: 'replace-loader',
					options: {
						flags: 'g',
						regex: '\/assets\/',
						sub: '\.\.\/assets\/'
					}
				}, {
					loader: "fontgen-loader",
					options: {
						fileName: 'assets/fonts/[fontname][ext]'
					}
				}]
			})
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
		}, {
			test: /\.(eot|ttf|woff|woff2|svg)$/,
			use: [{
				loader: "file-loader",
				options: {
					name: "assets/fonts/[name].[ext]"
				}
			}]
		}]
	},
	plugins: [
		new BundleTracker({filename: './webpack-stats.json'}),
		new webpack.DefinePlugin({
			"process.env": {
				"NODE_ENV": JSON.stringify("production")
			}
		}),
		extractIcons,
		extractStyles,
		//new webpack.optimize.UglifyJsPlugin()
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