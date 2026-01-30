module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'ops/exporters/**/*.js',
    '!ops/exporters/**/*.test.js'
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
    '**/validation/agent_exports/**/*.test.js'
  ],
  verbose: true
};
