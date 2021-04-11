import useSWR from "swr";
const fetcher = (...args) => (
    fetch(...args).then(
        response => {
          if (!response.ok) {
            throw new Error(response.statusText);
          }
          return response.json();
        }
      )
);

export function useBS() {
    const {data, error, isValidating} = useSWR(`/bullshit`, fetcher);

    return {
        quote: data ? data.bullshit : undefined,
        isLoading: isValidating,
        error
    }
}

export function useInputSource (id) {
    const { data, error, isValidating } = useSWR(`/input-file/${id}`, fetcher);

    return {
        inputSource: data,
        isValidating,
        error
    }
}