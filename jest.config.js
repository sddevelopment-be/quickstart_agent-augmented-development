module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'tools/exporters/**/*.js',
    'tools/scripts/deploy-skills.js',
    '!tools/exporters/**/*.test.js',
    '!tests/integration/**/*.js'
  ],
  coverageThreshold: {
    global: {
      branches: 84,
      functions: 85,
      lines: 85,
      statements: 85
    }
  },
  testMatch: [
    '**/tests/unit/**/*.test.js',
    '**/tests/integration/exporters/**/*.test.js',
    '**/tests/integration/**/*.test.js'
  ],
  verbose: true
};
