# Minikube

在學習 Kubernetes（K8s）之前，很多人會聽到一個工具叫做 **Minikube**。這篇文章會告訴你：

- Minikube 是什麼？
- 它與 Kubernetes 和 Docker 有什麼關係？
- 如何在 macOS 上安裝 Minikube？
- 啟動後發生了什麼事？

## 什麼是 Minikube？它是做什麼用的？為什麼需要它？

Minikube 是一個輕量級的工具，用來在**本機（local）電腦**上建立一個小型的 Kubernetes 叢集（cluster）。它讓你可以：

- 練習和學習 Kubernetes 指令與概念
- 本機測試 Kubernetes 部署（例如 Ingress、Pod、Service、Volume 等）
- 建立開發環境，模擬雲端部署前的操作

如果你沒有雲端帳號（像是 GCP、AWS），或者不想每次測試都上雲端，**Minikube 就是一個很好的選擇**。

## Minikube、Kubernetes、Docker 之間的關係

| 工具名稱      | 功能簡介                                               | 舉例說明                     |
|---------------|--------------------------------------------------------|------------------------------|
| Docker        | 容器工具，幫你打包應用程式和依賴環境                   | 把一個 Flask 應用包成 image |
| Kubernetes    | 容器編排系統，幫你自動化管理大量 container 運行狀況     | 自動分配資源、重啟異常服務   |
| Minikube      | 在你本機上模擬一個小型 Kubernetes 環境                | 測試 K8s 設定是否正確        |

簡單來說：

- **Docker** 是裝應用的「容器」。
- **Kubernetes** 是負責「管容器」的系統。
- **Minikube** 則是讓你「在自己電腦上跑 Kubernetes」的工具。

## 如何在 macOS 上安裝 Minikube

1. **先確認安裝條件**：
   - macOS 10.13 以上
   - 已安裝 Homebrew
   - 已安裝虛擬化環境（建議使用 Docker Desktop）

2. **使用 Homebrew 安裝 Minikube**：

    ```bash
    brew install minikube
    ```

3. **確認安裝完成**：

    ```bash
    minikube version
    ```

4. **啟動 Minikube**：

    ```bash
    minikube start
    ```

## 啟動 Minikube 後發生了什麼事？

當你執行 `minikube start` 時，系統會做以下幾件事：

1. **建立一個 VM 或 Container**：
   - 預設使用 Docker driver，它會透過 Docker 建立一個模擬 Kubernetes 的環境。

2. **下載 Kubernetes 所需元件**：
   - 包括 kube-apiserver、kubelet、etcd 等，模擬一個控制平面。

3. **啟動 Kubernetes 叢集**：
   - Minikube 幫你開啟一個「單節點」的 K8s 叢集。

4. **設定 kubectl 指向本機叢集**：
   - 這樣你可以直接用 `kubectl` 對 Minikube 發指令。

5. **建立 dashboard（可選）**：

    ```bash
    minikube dashboard
    ```

    這會開啟瀏覽器介面，讓你視覺化地觀察 Pod、Service 等狀態。

## 小結

Minikube 是 Kubernetes 的學習好幫手，適合本機練習與開發。你可以透過它快速：

- 建立測試環境
- 練習 YAML 檔部署
- 練習 CI/CD 或 DevOps 工作流程