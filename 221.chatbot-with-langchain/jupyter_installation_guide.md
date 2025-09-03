# Jupyter Notebook 설치 가이드

## 목차
- [사전 요구사항](#사전-요구사항)
- [Python 설치](#python-설치)
- [UV를 사용한 빠른 설치 (권장)](#uv를-사용한-빠른-설치-권장)
- [Jupyter Notebook 설치](#jupyter-notebook-설치)
- [가상환경 설정 (권장)](#가상환경-설정-권장)
- [Jupyter Lab 설치 (선택)](#jupyter-lab-설치-선택)
- [실행 및 확인](#실행-및-확인)
- [트러블슈팅](#트러블슈팅)

---

## 사전 요구사항

- Python 3.7 이상
- pip (Python 패키지 매니저)
- 인터넷 연결

---

## Python 설치

### 🍎 macOS

#### 방법 1: 공식 Python.org에서 설치
```bash
# Python.org에서 최신 버전 다운로드
# https://www.python.org/downloads/

# Homebrew를 이용한 설치 (권장)
brew install python3
```

#### 방법 2: Homebrew 사용
```bash
# Homebrew가 설치되어 있지 않다면
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Python 설치
brew install python3
```

#### Python 설치 확인
```bash
python3 --version
pip3 --version
```

### 🪟 Windows

#### 방법 1: 공식 Python.org에서 설치
1. https://www.python.org/downloads/ 접속
2. 최신 Python 버전 다운로드
3. 설치 시 **"Add Python to PATH"** 체크박스 반드시 선택
4. "Install Now" 클릭

#### 방법 2: Microsoft Store에서 설치
```powershell
# Windows 10/11에서 Microsoft Store 앱 검색 후 "Python" 설치
```

#### 방법 3: Chocolatey 사용
```powershell
# PowerShell을 관리자 권한으로 실행
# Chocolatey가 설치되어 있지 않다면
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Python 설치
choco install python3
```

#### Python 설치 확인
```cmd
python --version
pip --version
```

---

## UV를 사용한 빠른 설치 (권장)

UV는 Rust로 작성된 빠른 Python 패키지 매니저입니다. pip보다 10-100배 빠르며 현대적인 Python 개발 환경을 제공합니다.

### UV 설치

#### 🍎 macOS

```bash
# Homebrew를 사용한 설치 (권장)
brew install uv

# 또는 curl을 사용한 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 설치 확인
uv --version
```

#### 🪟 Windows

```powershell
# PowerShell에서 설치
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# 또는 pip를 사용한 설치
pip install uv

# 설치 확인
uv --version
```

### UV를 사용한 Jupyter 프로젝트 설정

#### 🍎 macOS & 🪟 Windows 공통

```bash
# 1. 새 프로젝트 디렉토리 생성
mkdir my_jupyter_project
cd my_jupyter_project

# 2. Python 프로젝트 초기화
uv init

# 3. Python 버전 지정 (선택사항)
uv python pin 3.12

# 4. Jupyter 설치
uv add jupyter

# 5. 추가 데이터 과학 패키지 설치
uv add numpy pandas matplotlib seaborn plotly

# 6. 머신러닝 패키지 설치 (필요시)
uv add scikit-learn

# 7. LangChain 패키지 설치 (AI/LLM 작업시)
uv add langchain langchain-openai langchain-google-genai

# 8. 개발 의존성 추가 (중요!)
uv add --dev ipykernel jupyterlab

# 9. Python 커널 등록 (Jupyter에서 가상환경 인식용)
uv run python -m ipykernel install --user --name my_jupyter_project

# 10. Jupyter 실행
uv run jupyter notebook
# 또는 Jupyter Lab 실행
uv run jupyter lab
```

### UV 주요 장점

✅ **속도**: pip보다 10-100배 빠른 패키지 설치  
✅ **의존성 관리**: 자동으로 의존성 충돌 해결  
✅ **가상환경**: 자동으로 프로젝트별 가상환경 생성  
✅ **Python 버전 관리**: 여러 Python 버전 자동 관리  
✅ **Lock 파일**: `uv.lock` 파일로 정확한 버전 고정  

### UV 유용한 명령어

```bash
# 패키지 추가
uv add package_name

# 개발 의존성 추가
uv add --dev package_name

# 패키지 제거
uv remove package_name

# 모든 의존성 설치
uv sync

# Python 스크립트 실행
uv run python script.py

# 가상환경 활성화
source .venv/bin/activate  # macOS
# 또는
.venv\Scripts\activate     # Windows

# 프로젝트 정보 확인
uv tree

# Jupyter 커널 관리
uv run python -m ipykernel install --user --name project_name  # 커널 등록
jupyter kernelspec list  # 설치된 커널 확인
jupyter kernelspec remove project_name  # 커널 제거
```

### pyproject.toml 예시

UV 사용 시 자동 생성되는 `pyproject.toml` 파일 예시:

```toml
[project]
name = "my-jupyter-project"
version = "0.1.0"
description = "Jupyter notebook project with UV"
readme = "README.md"
requires-python = ">=3.8"
dependencies = [
    "jupyter>=1.0.0",
    "numpy>=1.24.0",
    "pandas>=2.0.0",
    "matplotlib>=3.7.0",
    "seaborn>=0.12.0",
]

[project.optional-dependencies]
ml = [
    "scikit-learn>=1.3.0",
    "tensorflow>=2.13.0",
]
llm = [
    "langchain>=0.1.0",
    "langchain-openai>=0.1.0",
    "langchain-google-genai>=1.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

---

## Jupyter Notebook 설치

### 🍎 macOS

#### 기본 설치
```bash
# pip를 이용한 설치
pip3 install jupyter

# 또는 pip3가 기본 pip라면
pip install jupyter
```

#### Conda를 사용하는 경우
```bash
# Anaconda/Miniconda가 설치되어 있다면
conda install jupyter
```

### 🪟 Windows

#### 기본 설치
```cmd
# Command Prompt 또는 PowerShell에서 실행
pip install jupyter
```

#### Conda를 사용하는 경우
```cmd
# Anaconda Prompt에서 실행
conda install jupyter
```

---

## 가상환경 설정 (권장)

프로젝트별로 독립적인 패키지 환경을 만들어 충돌을 방지합니다.

### 🍎 macOS

```bash
# 1. 프로젝트 디렉토리 생성 및 이동
mkdir my_jupyter_project
cd my_jupyter_project

# 2. 가상환경 생성
python3 -m venv jupyter_env

# 3. 가상환경 활성화
source jupyter_env/bin/activate

# 4. pip 업그레이드
pip install --upgrade pip

# 5. Jupyter 설치
pip install jupyter

# 6. 추가 패키지 설치 (필요한 경우)
pip install numpy pandas matplotlib seaborn scikit-learn

# 7. 가상환경 비활성화 (작업 완료 후)
deactivate
```

### 🪟 Windows

```cmd
# 1. 프로젝트 디렉토리 생성 및 이동
mkdir my_jupyter_project
cd my_jupyter_project

# 2. 가상환경 생성
python -m venv jupyter_env

# 3. 가상환경 활성화
jupyter_env\Scripts\activate

# 4. pip 업그레이드
python -m pip install --upgrade pip

# 5. Jupyter 설치
pip install jupyter

# 6. 추가 패키지 설치 (필요한 경우)
pip install numpy pandas matplotlib seaborn scikit-learn

# 7. 가상환경 비활성화 (작업 완료 후)
deactivate
```

---

## Jupyter Lab 설치 (선택)

Jupyter Lab은 Jupyter Notebook의 차세대 버전으로 더 많은 기능을 제공합니다.

### 🍎 macOS & 🪟 Windows 공통

```bash
# Jupyter Lab 설치
pip install jupyterlab

# 또는 Jupyter Notebook과 함께 설치
pip install jupyter jupyterlab
```

---

## 실행 및 확인

### Jupyter Notebook 실행

#### 🍎 macOS
```bash
# 가상환경이 활성화된 상태에서
jupyter notebook

# 특정 포트에서 실행
jupyter notebook --port=8889

# 브라우저 자동 실행 비활성화
jupyter notebook --no-browser
```

#### 🪟 Windows
```cmd
# Command Prompt에서 (가상환경 활성화된 상태)
jupyter notebook

# 또는 PowerShell에서
jupyter notebook

# 특정 포트에서 실행
jupyter notebook --port=8889
```

### Jupyter Lab 실행

```bash
# 가상환경이 활성화된 상태에서
jupyter lab

# 특정 포트에서 실행
jupyter lab --port=8889
```

### 브라우저에서 확인

실행 후 브라우저에서 자동으로 열리며, 다음 주소로 접근 가능합니다:
- `http://localhost:8888` (기본 포트)
- `http://127.0.0.1:8888`

---

## 유용한 Jupyter 확장 기능

### Jupyter Notebook Extensions 설치

#### 기존 pip 사용
```bash
# nbextensions 설치
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user

# nbextensions configurator 설치
pip install jupyter_nbextensions_configurator
jupyter nbextensions_configurator enable --user
```

#### UV 사용 (권장)
```bash
# 개발 의존성으로 추가
uv add --dev jupyter_contrib_nbextensions jupyter_nbextensions_configurator

# 확장 설치
uv run jupyter contrib nbextension install --user
uv run jupyter nbextensions_configurator enable --user
```

### 자주 사용되는 패키지들

#### 기존 pip 사용
```bash
# 데이터 과학 패키지
pip install numpy pandas matplotlib seaborn plotly

# 머신러닝 패키지
pip install scikit-learn tensorflow keras pytorch

# 웹 스크래핑
pip install requests beautifulsoup4

# LangChain (AI/LLM 관련)
pip install langchain langchain-openai langchain-google-genai
```

#### UV 사용 (권장)
```bash
# 데이터 과학 패키지 한번에 설치
uv add numpy pandas matplotlib seaborn plotly

# 머신러닝 패키지
uv add scikit-learn tensorflow keras torch

# 웹 스크래핑
uv add requests beautifulsoup4 lxml

# LangChain (AI/LLM 관련)
uv add langchain langchain-openai langchain-google-genai

# 선택적 의존성 그룹으로 설치
uv add --optional ml scikit-learn tensorflow
uv add --optional llm langchain langchain-openai
```

---

## 트러블슈팅

### ⚡ UV 관련 문제 해결

#### 1. UV 설치 실패
```bash
# 🍎 macOS
# Homebrew 업데이트 후 재설치
brew update && brew upgrade && brew install uv

# curl 직접 설치 시도
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # 또는 source ~/.zshrc

# 🪟 Windows  
# PowerShell 실행 정책 변경 후 재시도
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 2. 'uv' 명령어를 찾을 수 없음
```bash
# 🍎 macOS
# PATH에 uv 추가
echo 'export PATH="$HOME/.cargo/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# 🪟 Windows
# 사용자 환경변수 PATH에 추가
# %USERPROFILE%\.cargo\bin
```

#### 3. Python 버전 문제
```bash
# 사용 가능한 Python 버전 확인
uv python list

# 특정 Python 버전 설치
uv python install 3.12

# 프로젝트에 Python 버전 고정
uv python pin 3.12
```

#### 4. 패키지 설치 실패
```bash
# 캐시 정리 후 재시도
uv cache clean

# 의존성 다시 동기화
uv sync --reinstall

# 특정 패키지 강제 재설치
uv add --force-reinstall package_name
```

#### 5. Jupyter 실행 안됨
```bash
# UV를 통한 실행 시도
uv run jupyter notebook

# ipykernel이 없는 경우 설치
uv add --dev ipykernel
uv run python -m ipykernel install --user --name my_project

# 가상환경 활성화 후 실행
source .venv/bin/activate  # macOS
.venv\Scripts\activate     # Windows
jupyter notebook

# 포트 문제 시 다른 포트 사용
uv run jupyter notebook --port=8889
```

#### 7. Jupyter에서 가상환경 커널이 안 보임
```bash
# 커널 등록 확인
jupyter kernelspec list

# 커널이 없다면 수동 등록
uv run python -m ipykernel install --user --name my_project --display-name "Python (my_project)"

# 기존 커널 제거 후 재등록
jupyter kernelspec remove my_project
uv run python -m ipykernel install --user --name my_project
```

#### 6. 의존성 충돌 문제
```bash
# 의존성 트리 확인
uv tree

# Lock 파일 재생성
rm uv.lock
uv lock

# 깨끗한 환경에서 재설치
rm -rf .venv
uv sync
```

### 🍎 macOS 문제 해결

#### 1. Permission 에러
```bash
# pip 권한 문제 시
pip3 install --user jupyter
```

#### 2. Command not found
```bash
# ~/.bash_profile 또는 ~/.zshrc에 PATH 추가
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc
source ~/.zshrc
```

#### 3. SSL Certificate 에러
```bash
# 인증서 문제 시
pip3 install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org jupyter
```

### 🪟 Windows 문제 해결

#### 1. 'python'이 내부 또는 외부 명령이 아닙니다
```cmd
# Python PATH 확인 및 추가
# 시스템 환경변수 PATH에 Python 설치 경로 추가
# 예: C:\Users\[username]\AppData\Local\Programs\Python\Python311\
# 예: C:\Users\[username]\AppData\Local\Programs\Python\Python311\Scripts\
```

#### 2. pip 업그레이드 문제
```cmd
# Python을 명시적으로 호출
python -m pip install --upgrade pip
```

#### 3. 방화벽/백신 문제
```cmd
# 특정 호스트 신뢰
pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org jupyter
```

#### 4. PowerShell 실행 정책 문제
```powershell
# PowerShell을 관리자 권한으로 실행 후
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 종료 방법

### Jupyter 종료
- 브라우저에서 Jupyter 탭 닫기
- 터미널/Command Prompt에서 `Ctrl + C` 두 번 입력
- `y` 입력하여 종료 확인

### 가상환경 종료
```bash
# macOS/Linux
deactivate

# Windows
deactivate
```

---

## 참고 자료

### 공식 문서
- [Jupyter 공식 문서](https://jupyter.org/documentation)
- [Jupyter Notebook 문서](https://jupyter-notebook.readthedocs.io/)
- [JupyterLab 문서](https://jupyterlab.readthedocs.io/)
- [Python 가상환경 가이드](https://docs.python.org/3/tutorial/venv.html)

### UV 관련
- [UV 공식 문서](https://docs.astral.sh/uv/)
- [UV GitHub 저장소](https://github.com/astral-sh/uv)
- [UV 설치 가이드](https://docs.astral.sh/uv/getting-started/installation/)
- [pyproject.toml 가이드](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)

---

**💡 팁**: 
- **UV 사용 권장**: 빠른 속도와 현대적인 의존성 관리로 UV 사용을 강력히 권장합니다.
- **프로젝트 격리**: 프로젝트별로 가상환경을 사용하여 의존성 충돌을 방지하세요.
- **Jupyter Lab 우선**: 더 현대적인 인터페이스를 제공하므로 새 프로젝트에서는 Lab 사용을 고려해보세요.
- **정기 업데이트**: 
  - UV: `uv self update`
  - pip: `pip install --upgrade jupyter`
- **Lock 파일 관리**: `uv.lock` 파일을 git에 포함시켜 팀원들과 동일한 환경을 공유하세요.
- **선택적 의존성**: 프로젝트 규모에 따라 `[project.optional-dependencies]`를 활용하여 필요한 패키지만 설치하세요.