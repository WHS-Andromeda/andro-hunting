import os
import sys
from datetime import datetime


class Logger:
    def __init__(self, logDir="./logs", runLogFile=None, errorLogFile=None):
        self.logDir = logDir
        self.runLogFile = runLogFile or self._generateLogFilename("run")
        self.errorLogFile = errorLogFile or self._generateLogFilename("error")
        self._ensureLogDirectory()
        self.runLogFilePath = os.path.join(self.logDir, self.runLogFile)
        self.errorLogFilePath = os.path.join(self.logDir, self.errorLogFile)
        self._originalStdout = sys.stdout
        self._originalStderr = sys.stderr

    def _ensureLogDirectory(self):
        """로그 디렉터리 생성"""
        if not os.path.exists(self.logDir):
            os.makedirs(self.logDir)

    def _generateLogFilename(self, logType):
        """로그 파일명 생성"""
        currentTime = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{logType}_log_{currentTime}.txt"

    def startLoggingSession(self):
        """로그 세션 시작, stdout과 stderr 리다이렉트"""
        sys.stdout = open(self.runLogFilePath, "w")
        sys.stderr = open(self.errorLogFilePath, "w")
        print(
            f"Logging session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        print(f"Run log file: {self.runLogFilePath}")
        print(f"Error log file: {self.errorLogFilePath}", file=sys.stderr)

    def stopLoggingSession(self):
        """로그 세션 종료, stdout과 stderr 복원"""
        if sys.stdout != self._originalStdout:
            sys.stdout.close()
            sys.stdout = self._originalStdout
        if sys.stderr != self._originalStderr:
            sys.stderr.close()
            sys.stderr = self._originalStderr
        print(f"Logging session ended. Run log saved to {self.runLogFilePath}")
        print(f"Error log saved to {self.errorLogFilePath}", file=sys.stderr)

    def log(self, message, isError=False):
        """메시지를 로그에 기록"""
        logFilePath = self.errorLogFilePath if isError else self.runLogFilePath
        with open(logFilePath, "a") as f:
            currentTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{currentTime} - {message}\n")


def logError(packageName):
    """에러 로그 기록"""
    logger = Logger()
    logger.log(packageName, isError=True)


def logRun(message):
    """실행 로그 기록"""
    logger = Logger()
    logger.log(message)
