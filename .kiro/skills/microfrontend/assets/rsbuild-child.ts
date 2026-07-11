/* eslint-disable @typescript-eslint/no-explicit-any */
import { defineConfig } from '@rsbuild/core';
import { pluginReact } from '@rsbuild/plugin-react';
import { pluginModuleFederation } from '@module-federation/rsbuild-plugin';
import JavaScriptObfuscator from 'javascript-obfuscator';
import { generateVersionFile } from './src/shared/utils/generateVersionFile';
import { dependencies as deps, version } from './package.json';

const isDev = process.env.NODE_ENV === 'development';
const port = parseInt(process.env.PORT || '3001') || 3001;
const assetPrefix = process.env.ASSET_PREFIX || 'auto';
const hostUrl = process.env.HOST_URL || 'http://localhost:3000';
const mode = isDev ? 'development' : 'production';

export default defineConfig({
  mode,
  server: {
    port,
  },
  source: {
    entry: {
      index: './src/main.tsx',
    },
  },
  output: {
    assetPrefix,
    distPath: {
      js: '',
      css: '',
    },
    filename: {
      js: '[name].[contenthash].js',
      css: '[name].[contenthash].css',
    },
    legalComments: 'none',
    sourceMap: {
      js: isDev ? 'cheap-module-source-map' : false,
      css: isDev,
    },
  },
  performance: {
    chunkSplit: {
      strategy: 'split-by-experience',
      override: {
        cacheGroups: {
          'vendor-react': {
            test: /node_modules[\\/](react|react-dom|react-router-dom)[\\/]/,
            priority: 30,
            name: 'vendor-react',
          },
          'vendor-toast': {
            test: /node_modules[\\/]react-toastify/,
            priority: 20,
            name: 'vendor-toast',
          },
          vendor: {
            test: /node_modules/,
            priority: 10,
            name: 'vendor',
          },
        },
      },
    },
  },
  plugins: [
    pluginReact(),
    pluginModuleFederation({
      dts: false,
      name: '{modulename}',           // lowercase English, unique per child
      filename: 'mf-entry.js',
      exposes: {
        './App': './src/App',         // Only expose App
      },
      remotes: {
        host: `host@${hostUrl}/mf-entry.js`,
      },
      shared: {
        react: { singleton: true, eager: false, requiredVersion: deps.react },
        'react-dom': { singleton: true, eager: false, requiredVersion: deps['react-dom'] },
        'react-router-dom': { singleton: true, eager: false, requiredVersion: deps['react-router-dom'] },
        antd: { singleton: true, eager: false, requiredVersion: deps.antd },
        dayjs: { singleton: true, eager: false, requiredVersion: deps.dayjs },
        '@tanstack/react-query': { singleton: true, eager: false },
      },
    }),
    generateVersionFile('{modulename}', version),
  ],
  tools: {
    htmlPlugin: false,  // Child doesn't generate HTML
    rspack(config) {
      // Obfuscation for production builds
      if (!isDev) {
        config.plugins.push({
          apply(compiler: any) {
            compiler.hooks.emit.tap('ObfuscatorPlugin', (compilation: any) => {
              for (const assetName of Object.keys(compilation.assets)) {
                if (assetName.endsWith('.js')) {
                  const source = compilation.assets[assetName].source().toString();
                  const obfuscated = JavaScriptObfuscator.obfuscate(source, {
                    compact: true,
                    controlFlowFlattening: false,
                    deadCodeInjection: false,
                    debugProtection: true,
                    debugProtectionInterval: 4000,
                    disableConsoleOutput: true,
                    identifierNamesGenerator: 'hexadecimal',
                    numbersToExpressions: false,
                    renameGlobals: false,
                    selfDefending: false,
                    simplify: false,
                    splitStrings: false,
                    stringArray: true,
                    transformObjectKeys: false,
                    stringArrayCallsTransform: false,
                    stringArrayEncoding: ['base64'],
                    stringArrayIndexShift: false,
                    stringArrayRotate: false,
                    stringArrayShuffle: false,
                    stringArrayWrappersCount: 200,
                    stringArrayWrappersChainedCalls: false,
                    stringArrayWrappersParametersMaxCount: 200,
                    stringArrayWrappersType: 'variable',
                    stringArrayThreshold: 1,
                    unicodeEscapeSequence: false,
                    renamePropertiesMode: 'safe',
                    renameProperties: false,
                  });
                  const code = obfuscated.getObfuscatedCode();
                  compilation.updateAsset(assetName, {
                    source: () => code,
                    size: () => code.length,
                  });
                }
              }
            });
          },
        });
      }
    },
  },
});
