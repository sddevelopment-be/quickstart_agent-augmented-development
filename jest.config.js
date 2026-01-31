module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'ops/exporters/**/*.js',
    'ops/deploy-skills.js',
    '!ops/exporters/**/*.test.js',
    '!ops/__tests__/**/*.js'
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
    '**/validation/agent_exports/**/*.test.js',
    '**/ops/__tests__/**/*.test.js'
  ],
  verbose: true
};
