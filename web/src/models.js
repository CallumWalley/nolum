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
    const {data, error, isValidating} = useSWR(`/bullshit`, fetcher, {
      revalidateOnFocus: false
    });

    return {
        quote: data ? data.bullshit : undefined,
        isLoading: isValidating,
        error
    }
}

export function useInputSource (id = "") {
  const url = id !== "" ? `/input-files/${id}` : "/input-files"
    const { data, error, isValidating } = useSWR(url, fetcher);

    return {
        inputSource: data ? data.list : undefined,
        isValidating,
        error
    }
}