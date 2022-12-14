import cn from 'classnames'
import Image from 'next/image'
import { useRouter } from 'next/router'
import { useForm } from 'react-hook-form'
import { createJob } from 'tools/client'

type Props = {}

function CreateMain({}: Props) {
  const router = useRouter()

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm()
  const onSubmit = async (data: any, e: any) => {
    e.preventDefault()
    const job = await createJob(data)
    router.push(`/basins/${job.id}`)
  }

  const inputPairs = [
    {
      left: {
        name: 'basinName',
        title: 'name',
        placeholder: 'Mr Newton',
      },
      right: {
        name: 'coefs',
        title: 'coefs',
        placeholder: '[1, 0, 2, 0, 1]',
      },
    },
    {
      left: {
        name: 'imw',
        title: 'imw',
        placeholder: '128',
      },
      right: {
        name: 'imh',
        title: 'imh',
        placeholder: '128',
      },
    },
    {
      left: {
        name: 'crmin',
        title: 'crmin',
        placeholder: '-1.0',
      },
      right: {
        name: 'crmax',
        title: 'crmax',
        placeholder: '1.0',
      },
    },
    {
      left: {
        name: 'cimin',
        title: 'cimin',
        placeholder: '-1.0',
      },
      right: {
        name: 'cimax',
        title: 'cimax',
        placeholder: '1.0',
      },
    },
    {
      left: {
        name: 'itmax',
        title: 'itmax',
        placeholder: '30',
      },
      right: {
        name: 'tol',
        title: 'tol',
        placeholder: '1e-6',
      },
    },
  ]

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {/* main section */}
      <main className="p-4">
        <div className="flex w-full max-w-4xl md:flex-row max-md:flex-col">
          <div className="p-4 border rounded-lg border-primary basis-1/2">
            <h1 className="text-lg">Parameters</h1>

            {inputPairs.map((item, index) => {
              return (
                <div key={index} className="flex flex-row ">
                  {/* left inputs */}
                  {item.left && (
                    <div className="m-2 basis-1/2">
                      <div className="w-full max-w-xs form-control">
                        <label className="label">
                          <span className="label-text">{item.left.title}</span>
                        </label>
                        <input
                          type="text"
                          placeholder={item.left.placeholder}
                          className={cn([
                            'w-full',
                            'max-w-xs',
                            'input',
                            'input-bordered',
                            { 'input-error': errors?.[item.left.name] },
                          ])}
                          {...register(item.left.name, { required: true })}
                        />
                      </div>
                    </div>
                  )}

                  {/* right inputs */}
                  {item.right && (
                    <div className="m-2 basis-1/2">
                      <div className="w-full max-w-xs form-control">
                        <label className="label">
                          <span className="label-text">{item.right.title}</span>
                        </label>
                        <input
                          type="text"
                          placeholder={item.right.placeholder}
                          className={cn([
                            'w-full',
                            'max-w-xs',
                            'input',
                            'input-bordered',
                            { 'input-error': errors?.[item.right.name] },
                          ])}
                          {...register(item.right.name, { required: true })}
                        />
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>

          <div className="relative p-4 border rounded-lg border-primary basis-1/2">
            <h1 className="text-lg">Preview</h1>

            <Image src="/logo.svg" alt="preview" width="500" height="500" />
          </div>
        </div>

        <div className="">
          <button
            className="my-2 mr-2 btn btn-outline"
            onClick={() => {
              router.push('/basins')
            }}
          >
            Cancel
          </button>
          <button type="submit" className="my-2 btn btn-primary">
            Create
          </button>
        </div>
      </main>
    </form>
  )
}

export default CreateMain
