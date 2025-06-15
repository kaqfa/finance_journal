module.exports = {
  extends: [
    "./index.js",
    "next/core-web-vitals",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  settings: {
    react: {
      version: "detect"
    }
  },
  env: {
    browser: true,
    node: true
  },
  rules: {
    "react/react-in-jsx-scope": "off",
    "react/prop-types": "off"
  }
};